import pandas as pd
from math import sqrt
from . import preprocessing
from . import academics
from . import persona
from . import predict_score
# 3-cluster model centroids (Academic Performance)
CENTROID3 = {
    'cluster1': [0.26407826, 0.4980978], 
    'cluster2': [0.28523119, 0.83384127], 
    'cluster3': [0.24843434, 0.16748274] 
}

# 5-cluster model centroids (Behavioural Personas)
CENTROID5 = {
    'cluster1': [0.48434735, 0.51876055, 0.35172773, 0.32871612, 0.69163936], 
    'cluster2': [0.47051680, 0.51762281, 0.72973323, 0.31982215, 0.69597686], 
    'cluster3': [0.47009039, 0.51307385, 0.73488024, 0.67072522, 0.73466401], 
    'cluster4': [0.47551055, 0.50872846, 0.34926632, 0.67422251, 0.72645642], 
    'cluster5': [0.47012020, 0.51000000, 0.50000000, 0.50000000, 0.50000000] 
}

def get_complete_analysis(data):
    """
    Main entry point for the dashboard.
    Handles both a single student dict or a full DataFrame.
    """
    
    # CASE 1: Single Student (Dictionary from Form)
    if isinstance(data, dict):
        mode="analyse"
        if data.get('Exam_Score',None):
            # basically if the key has a value
            pass
            # basically that means you are not doing predictive analysis 
        else:
            # run a function that predict's using mayank's model
            # change Exam_Scores value to the predicted value
            # have a way to know that the prediction function ran
            mode="predict"
            data["Exam_Score"]=predict_score.predict_exam_score(data)

        # now u will definitely have 20 non empty values
        scaled_record = preprocessing.scale_single_record(data)
        
        # 2. Extract academic pair for 3-cluster model
        # Use existing utility from academics.py
        data3 = academics.pick2rec(scaled_record)
        point3 = [data3['Exam_Score'], data3['Previous_Scores']]
        
        # 3. Reduce to 5 themes for persona model
        data5 = persona.reduce_record(scaled_record)
        point5 = [
            data5['Academic_Drive'], data5['Resource_Access'], 
            data5['Family_Capital'], data5['Personal_Wellbeing'], 
            data5['Environmental_Stability']
        ]
        
        # 4. Find closest clusters
        def find_best(pt, centers):
            best = None
            min_d = float('inf')
            for name, coords in centers.items():
                d = sum((a - b)**2 for a, b in zip(pt, coords))
                if d < min_d:
                    min_d = d
                    best = name
            return best

        return {"mode":mode,
            "academic_cluster": find_best(point3, CENTROID3),
            "persona_cluster": find_best(point5, CENTROID5)
        }

    # CASE 2: CSV Data (DataFrame)
    else:
        # check if the Exam_Score column is empty if so then use mayank's model to predict for each record and add this column to the the dataframe or the csv

        df = pd.read_csv(data)
        # Step A: Fill missing values in batch
        if 'Exam_Score' not in df.columns or df['Exam_Score'].isnull().any():
            df['Exam_Score'] = predict_exam_score(df)
        
        # 1. Preprocess the whole batch
        processed_df = preprocessing.scale_csv_file(df)
        
        # 2. Run academic clustering
        data3_df = academics.pick2rec(processed_df)
        academic_results = academics.predict_ac(data3_df, CENTROID3)
        
        # 3. Run persona clustering
        data5_df = persona.reduce_dataframe(processed_df)
        persona_results = persona.predict_pc(data5_df, CENTROID5)
        
        return {
            "academic_mapping": academic_results,
            "persona_mapping": persona_results
        }
        # output looks like this 
        # {"academic_mapping":{"cluster1": [indices],......"cluster5": [indices]},"persona_mapping":{"cluster1":[indices],....."cluster3":[indices]}}


def visualise(data):
    # for single student we show:
    # a spider chart (5 features)
    # his position in 5 cluster model(his persona type)
    # his position in 3 cluster model with color codes (red if they are in cluster 3, green if they are in cluster 2 and yellow if they are in cluster 1)
    # if we predict score then we show that too

    # for group
    # we show a pie chart containing the class composition based on 3 cluster model
    # we show a pie chart for all of the 3 academic clusters (basically we show a pie chart showing the 5 persona composition of every cluster we got from the 3 cluster model )
    pass

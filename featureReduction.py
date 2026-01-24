import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def reduce_to_five_themes(input_file, output_file):
    # 1. Load the numerically mapped data
    df = pd.read_csv(input_file)
    
    # 2. Invert "Negative" features so that 1.0 always = "Better for Success"
    # Distance: Near(0) is better than Far(2) -> Invert
    # Disabilities: No(0) is better than Yes(1) -> Invert
    df['Distance_from_Home'] = df['Distance_from_Home'].max() - df['Distance_from_Home']
    df['Learning_Disabilities'] = df['Learning_Disabilities'].max() - df['Learning_Disabilities']

    # 3. Scale all 19 predictors between 0 and 1
    # This ensures a "high score" in one category (like Previous_Scores 0-100) 
    # doesn't drown out a binary category (like Internet_Access 0-1).
    scaler = MinMaxScaler()
    predictor_cols = df.columns.difference(['Exam_Score'])
    df[predictor_cols] = scaler.fit_transform(df[predictor_cols])

    # 4. Create the 5 Thematic Features
    reduced_df = pd.DataFrame()

    # Theme 1: Academic Drive (Effort & Motivation)
    reduced_df['Academic_Drive'] = df[['Hours_Studied', 'Attendance', 
                                       'Previous_Scores', 'Motivation_Level']].mean(axis=1)

    # Theme 2: Resource Access (Socio-economic & School Tools)
    reduced_df['Resource_Access'] = df[['Access_to_Resources', 'Internet_Access', 
                                        'Tutoring_Sessions', 'Family_Income', 
                                        'Teacher_Quality', 'School_Type']].mean(axis=1)

    # Theme 3: Family Capital (Home Support)
    reduced_df['Family_Capital'] = df[['Parental_Involvement', 
                                       'Parental_Education_Level']].mean(axis=1)

    # Theme 4: Personal Wellbeing (Lifestyle)
    reduced_df['Personal_Wellbeing'] = df[['Sleep_Hours', 'Physical_Activity', 
                                           'Extracurricular_Activities']].mean(axis=1)

    # Theme 5: Environmental Stability (External Factors)
    reduced_df['Environmental_Stability'] = df[['Peer_Influence', 'Distance_from_Home', 
                                                'Learning_Disabilities']].mean(axis=1)

    # Keep the original Exam_Score as our target variable
    reduced_df['Exam_Score'] = df['Exam_Score']

    # 5. Save the final 5-dimension dataset
    reduced_df.to_csv(output_file, index=False)
    print(f"Successfully reduced 20 attributes to 5 themes. Saved to: {output_file}")
    return reduced_df

# Execute the script
reduced_data = reduce_to_five_themes('processeddata.csv', '5featuredata.csv')


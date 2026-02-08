# import pandas as pd
# from math import sqrt
# import os
# import json

# try:
#     from . import preprocessing
#     from . import academics
#     from . import persona
#     from . import predict_score
# except ImportError:
#     import preprocessing
#     import academics
#     import persona
#     import predict_score

# # 3-cluster model centroids (Academic Performance)
# CENTROID3 = {
#     'cluster1': [0.26407826, 0.4980978], # Yellow (Baseline)
#     'cluster2': [0.28523119, 0.83384127], # Green (High Growth)
#     'cluster3': [0.24843434, 0.16748274]  # Red (Critical)
# }

# # 5-cluster model centroids (Behavioural Personas)
# CENTROID5 = {
#     'cluster1': [0.48434735, 0.51876055, 0.35172773, 0.32871612, 0.69163936], 
#     'cluster2': [0.47051680, 0.51762281, 0.72973323, 0.31982215, 0.69597686], 
#     'cluster3': [0.47009039, 0.51307385, 0.73488024, 0.67072522, 0.73466401], 
#     'cluster4': [0.47050352, 0.52125862, 0.34757303, 0.67812502, 0.73516515],
#     'cluster5': [0.48512111, 0.51239632, 0.34586241, 0.32626084, 0.23126512]
# }

# def get_complete_analysis(data):
#     """
#     Coordination logic to get predictions and cluster assignments.
#     Tracks if the Exam_Score was predicted or provided.
#     """
#     if isinstance(data, dict):
#         raw_record = data.copy()
#         is_predicted = False
        
#         if 'Exam_Score' not in raw_record or raw_record['Exam_Score'] is None:
#             raw_record['Exam_Score'] = predict_score.predict_exam_score(raw_record)
#             is_predicted = True
        
#         scaled_record = preprocessing.scale_single_record(raw_record)
        
#         # Calculate Academic Cluster (3)
#         pt3 = [scaled_record['Exam_Score'], scaled_record['Previous_Scores']]
#         ac_cluster = min(CENTROID3.keys(), key=lambda k: sum((a-b)**2 for a,b in zip(pt3, CENTROID3[k])))
        
#         # Calculate Persona Cluster (5)
#         reduced = persona.reduce_record(scaled_record)
#         pt5 = [reduced[t] for t in ['Academic_Drive', 'Resource_Access', 'Family_Capital', 'Personal_Wellbeing', 'Environmental_Stability']]
#         pc_cluster = min(CENTROID5.keys(), key=lambda k: sum((a-b)**2 for a,b in zip(pt5, CENTROID5[k])))
        
#         return {
#             "mode": "single",
#             "predicted_score": raw_record['Exam_Score'],
#             "is_predicted": is_predicted,
#             "academic_cluster": ac_cluster,
#             "persona_cluster": pc_cluster,
#             "radar_data": reduced,
#             "scaled_data": scaled_record
#         }

#     else:
#         if isinstance(data, str):
#             df = pd.read_csv(data)
#         else:
#             df = data.copy()

#         is_predicted = False
#         if 'Exam_Score' not in df.columns or df['Exam_Score'].isnull().any():
#             df['Exam_Score'] = predict_score.predict_exam_score(df)
#             is_predicted = True
            
#         processed_df = preprocessing.scale_csv_file(df)
        
#         data3_df = academics.pick2rec(processed_df)
#         ac_map = academics.predict_ac(data3_df, CENTROID3)
        
#         data5_df = persona.reduce_dataframe(processed_df)
#         pc_map = persona.predict_pc(data5_df, CENTROID5)
        
#         return {
#             "mode": "batch",
#             "is_predicted": is_predicted,
#             "academic_mapping": ac_map,
#             "persona_mapping": pc_map,
#             "full_df": processed_df,
#             "reduced_df": data5_df
#         }

# def visualise(data):
#     """
#     Transforms analysis results into structured data for UI charts.
#     """
#     analysis = get_complete_analysis(data)
    
#     if analysis['mode'] == 'single':
#         colors = {"cluster1": "yellow", "cluster2": "green", "cluster3": "red"}
        
#         return {
#             "type": "single",
#             "score_value": round(analysis['predicted_score'], 2),
#             "is_predicted_score": analysis['is_predicted'],
#             "charts": {
#                 "spider_chart": {
#                     "data": [
#                         {"subject": k.replace('_', ' '), "value": round(v * 100, 2)} 
#                         for k, v in analysis['radar_data'].items()
#                     ]
#                 },
#                 "persona_info": {
#                     "type": analysis['persona_cluster'],
#                     "label": f"Persona Model Assignment: {analysis['persona_cluster']}"
#                 },
#                 "academic_info": {
#                     "cluster": analysis['academic_cluster'],
#                     "color": colors.get(analysis['academic_cluster'], "grey"),
#                     "coordinates": {
#                         "x": round(analysis['scaled_data']['Previous_Scores'] * 100, 2),
#                         "y": round(analysis['scaled_data']['Exam_Score'] * 100, 2)
#                     }
#                 }
#             }
#         }
    
#     else:
#         ac_map = analysis['academic_mapping']
#         pc_map = analysis['persona_mapping']
#         total_students = sum(len(v) for v in ac_map.values())

#         academic_pie = [
#             {"name": k, "value": len(v), "percentage": round((len(v)/total_students)*100, 2)}
#             for k, v in ac_map.items()
#         ]

#         persona_pie = [
#             {"name": k, "value": len(v), "percentage": round((len(v)/total_students)*100, 2)}
#             for k, v in pc_map.items()
#         ]

#         nested_breakdown = {}
#         for ac_key, ac_indices in ac_map.items():
#             breakdown = []
#             for pc_key, pc_indices in pc_map.items():
#                 intersection = set(ac_indices).intersection(set(pc_indices))
#                 if intersection:
#                     breakdown.append({
#                         "persona": pc_key,
#                         "count": len(intersection),
#                         "percentage": round((len(intersection)/len(ac_indices))*100, 2)
#                     })
#             nested_breakdown[ac_key] = breakdown

#         return {
#             "type": "batch",
#             "is_predicted_batch": analysis['is_predicted'],
#             "charts": {
#                 "academic_distribution": academic_pie,
#                 "overall_persona_distribution": persona_pie,
#                 "persona_per_academic_cluster": nested_breakdown
#             }
#         }
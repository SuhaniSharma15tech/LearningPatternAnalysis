import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# 1. Load the dataset (all 6,395 records)
df = pd.read_csv('newprocessed.csv')

# 2. Apply the mathematical reduction logic to every row
# This transforms the [a1...a34] vector into a [b1...b7] vector
reduced_data = pd.DataFrame()

# b1: Academic Momentum
reduced_data['Academic_Momentum'] = ((df['G1'] + df['G2'] + df['G3']) / 3) - (df['failures'] * 5)

# b2: Resilience & Grit
reduced_data['Resilience_Grit'] = df['studytime'] + df['higher'] + df['schoolsup'] + df['paid']

# b3: Support Stability
reduced_data['Support_Stability'] = ((df['Medu'] + df['Fedu']) / 2) + \
                                     ((df['Mjob'] + df['Fjob']) / 2) + \
                                     df['famsup'] + df['Pstatus']

# b4: Social Ecosystem
reduced_data['Social_Ecosystem'] = df['goout'] + df['romantic'] + df['activities'] + \
                                    df['internet'] + df['address']

# b5: Behavioral Risk (Inverting health: higher score = higher risk)
reduced_data['Behavioral_Risk'] = ((df['Dalc'] + df['Walc']) / 2) + (6 - df['health'])

# b6: Daily Friction (Normalizing absences to prevent skew)
reduced_data['Daily_Friction'] = df['age'] + df['traveltime'] + (df['absences'] / 10) + df['part_time_job']

# b7: Emotional Safety
reduced_data['Emotional_Safety'] = df['famrel'] + df['freetime'] + df['reason']

# 3. Scaling the 7 features between 0 and 1
# This ensures each of the 7 dimensions has equal weight in K-Means
scaler = MinMaxScaler()
final_matrix = scaler.fit_transform(reduced_data)
print(scaler.data_min_)
print(scaler.data_max_)
print(scaler.data_range_)
# # 4. Save the results
# # Each row in this CSV is an array of 7 values [b1, b2, b3, b4, b5, b6, b7]
df_final = pd.DataFrame(final_matrix, columns=reduced_data.columns)
df_final.to_csv('finalData.csv', index=False)

print(f"Successfully processed {len(df_final)} records.")
print("Each record is now a vector of 7 holistic values.")

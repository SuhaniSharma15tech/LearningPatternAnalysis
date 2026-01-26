# import numpy as np

# # These constants are derived from your 6,395 records to ensure 
# # the scaling is consistent with your trained model.
# GLOBAL_MIN_MAX = {
#     'Academic_Momentum': {'min': -13.666666666666666, 'max': 19.666666666666668},
#     'Resilience_Grit':   {'min': 1.0,                'max': 7.0},
#     'Support_Stability': {'min': 0.0,                'max': 10.0},
#     'Social_Ecosystem':  {'min': 1.0,                'max': 9.0},
#     'Behavioral_Risk':   {'min': 2.0,                'max': 10.0},
#     'Daily_Friction':    {'min': 16.0,               'max': 29.9},
#     'Emotional_Safety':  {'min': 2.0,                'max': 13.0}
# }

# def process_list(raw_list):
#     """
#     Input: List of 34 raw attributes [a1, a2, ... a34]
#     Output: List of 7 scaled dimensions [b1, b2, ... b7]
#     """
#     # 1. Column Mapping (Matches your unprocessed.csv order)
#     cols = [
#         'school', 'sex', 'age', 'address', 'famsize', 'Pstatus', 'Medu', 'Fedu',
#         'Mjob', 'Fjob', 'reason', 'guardian', 'traveltime', 'studytime', 'failures',
#         'schoolsup', 'famsup', 'paid', 'activities', 'nursery', 'higher', 
#         'internet', 'romantic', 'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 
#         'health', 'absences', 'G1', 'G2', 'G3', 'part_time_job'
#     ]
    
#     # Create a dictionary for logic processing
#     raw_dict = dict(zip(cols, raw_list))

#     # 2. Numerical Mapping
#     binary_map = {'yes': 1, 'no': 0, 'F': 1, 'M': 0, 'U': 1, 'R': 0, 
#                   'GT3': 1, 'LE3': 0, 'T': 1, 'A': 0, 'GP': 1, 'MS': 0}
#     job_map = {'teacher': 4, 'health': 3, 'services': 2, 'other': 1, 'at_home': 0}
#     reason_map = {'reputation': 3, 'course': 2, 'home': 1, 'other': 0}
    
#     p = {}
#     for key, val in raw_dict.items():
#         if val in binary_map:
#             p[key] = binary_map[val]
#         elif key in ['Mjob', 'Fjob']:
#             p[key] = job_map.get(val, 1)
#         elif key == 'reason':
#             p[key] = reason_map.get(val, 0)
#         else:
#             try:
#                 p[key] = float(val)
#             except:
#                 p[key] = 0

#     # 3. Mathematical Reduction to 7 Dimensions
#     b = {
#         'Academic_Momentum': ((p['G1'] + p['G2'] + p['G3']) / 3) - (p['failures'] * 5),
#         'Resilience_Grit': p['studytime'] + p['higher'] + p['schoolsup'] + p['paid'],
#         'Support_Stability': ((p['Medu'] + p['Fedu']) / 2) + ((p['Mjob'] + p['Fjob']) / 2) + p['famsup'] + p['Pstatus'],
#         'Social_Ecosystem': p['goout'] + p['romantic'] + p['activities'] + p['internet'] + p['address'],
#         'Behavioral_Risk': ((p['Dalc'] + p['Walc']) / 2) + (6 - p['health']),
#         'Daily_Friction': p['age'] + p['traveltime'] + (p['absences'] / 10) + p['part_time_job'],
#         'Emotional_Safety': p['famrel'] + p['freetime'] + p['reason']
#     }

#     # 4. Scaling and Output as List
#     order = ['Academic_Momentum', 'Resilience_Grit', 'Support_Stability', 
#              'Social_Ecosystem', 'Behavioral_Risk', 'Daily_Friction', 'Emotional_Safety']
    
#     final_list = []
#     for dim in order:
#         v_min = GLOBAL_MIN_MAX[dim]['min']
#         v_max = GLOBAL_MIN_MAX[dim]['max']
#         scaled = (b[dim] - v_min) / (v_max - v_min)
#         # Keep value strictly between 0 and 1
#         final_list.append(max(0.0, min(1.0, float(scaled))))

#     return final_list


# print(process_list(["MS","F",20,"R","LE3","A",1,2,"at_home","teacher","home","father",1,4,0,"yes","yes","no","yes","yes","no","no","no",5,2,1,4,5,2,10,14,15,16,"yes"]))

import numpy as np

# Constants derived from your processed.csv (649 records)
GLOBAL_MIN_MAX = {
    "Academic_Momentum": {"min": -13.666666666666666, "max": 19.666666666666668},
    "Resilience_Grit":   {"min": 1.0,                "max": 7.0},
    "Support_Stability": {"min": 0.0,                "max": 10.0},
    "Social_Ecosystem":  {"min": 1.0,                "max": 9.0},
    "Behavioral_Risk":   {"min": 2.0,                "max": 10.0},
    "Daily_Friction":    {"min": 16.0,               "max": 29.9},
    "Emotional_Safety":  {"min": 2.0,                "max": 13.0}
}

def process_dict_to_array(raw_dict):
    """
    Input: Dictionary { 'school': 'GP', 'sex': 'F', ... }
    Output: 1D NumPy Array [b1, b2, b3, b4, b5, b6, b7]
    """
    
    # 1. Numerical Mapping (Handling Categorical Inputs)
    binary_map = {'yes': 1, 'no': 0, 'f': 1, 'm': 0, 'u': 1, 'r': 0, 
                  'gt3': 1, 'le3': 0, 't': 1, 'a': 0, 'gp': 1, 'ms': 0}
    job_map = {'teacher': 4, 'health': 3, 'services': 2, 'other': 1, 'at_home': 0}
    reason_map = {'reputation': 3, 'course': 2, 'home': 1, 'other': 0}

    p = {}
    for key, val in raw_dict.items():
        # Clean string inputs for comparison
        clean_val = str(val).strip().lower() if isinstance(val, str) else val
        
        if clean_val in binary_map:
            p[key] = binary_map[clean_val]
        elif key in ['Mjob', 'Fjob']:
            p[key] = job_map.get(clean_val, 1)
        elif key == 'reason':
            p[key] = reason_map.get(clean_val, 0)
        else:
            try:
                p[key] = float(val)
            except (ValueError, TypeError):
                p[key] = 0.0

    # 2. Mathematical Reduction to 7 Dimensions
    # Note: Using .get() to prevent crashes if a key is missing from the dictionary
    b = {
        'Academic_Momentum': ((p.get('G1',0) + p.get('G2',0) + p.get('G3',0)) / 3) - (p.get('failures',0) * 5),
        'Resilience_Grit':   p.get('studytime',0) + p.get('higher',0) + p.get('schoolsup',0) + p.get('paid',0),
        'Support_Stability': ((p.get('Medu',0) + p.get('Fedu',0)) / 2) + ((p.get('Mjob',0) + p.get('Fjob',0)) / 2) + p.get('famsup',0) + p.get('Pstatus',0),
        'Social_Ecosystem':  p.get('goout',0) + p.get('romantic',0) + p.get('activities',0) + p.get('internet',0) + p.get('address',0),
        'Behavioral_Risk':   ((p.get('Dalc',0) + p.get('Walc',0)) / 2) + (6 - p.get('health',5)),
        'Daily_Friction':    p.get('age',0) + p.get('traveltime',0) + (p.get('absences',0) / 10) + p.get('part_time_job',0),
        'Emotional_Safety':  p.get('famrel',0) + p.get('freetime',0) + p.get('reason',0)
    }

    # 3. Scaling and Output as 1D NumPy Array
    order = ['Academic_Momentum', 'Resilience_Grit', 'Support_Stability', 
             'Social_Ecosystem', 'Behavioral_Risk', 'Daily_Friction', 'Emotional_Safety']
    
    final_array = []
    for dim in order:
        v_min = GLOBAL_MIN_MAX[dim]['min']
        v_max = GLOBAL_MIN_MAX[dim]['max']
        
        # Min-Max Scaler Formula: (x - min) / (max - min)
        scaled = (b[dim] - v_min) / (v_max - v_min)
        
        # Ensure values stay within [0, 1] range
        final_array.append(max(0.0, min(1.0, float(scaled))))

    return np.array(final_array)

# --- EXAMPLE DASHBOARD USAGE ---
if __name__ == "__main__":
    # Mock data from a dashboard form
    counselor_input = {
        'school': 'MS', 'sex': 'F', 'age': 20, 'address': 'R', 'famsize': 'LE3',
        'Pstatus': 'A', 'Medu': 1, 'Fedu': 2, 'Mjob': 'at_home', 'Fjob': 'teacher',
        'reason': 'home', 'guardian': 'father', 'traveltime': 1, 'studytime': 4,
        'failures': 0, 'schoolsup': 'yes', 'famsup': 'yes', 'paid': 'no',
        'activities': 'yes', 'nursery': 'yes', 'higher': 'no', 'internet': 'no',
        'romantic': 'no', 'famrel': 5, 'freetime': 2, 'goout': 1, 'Dalc': 4,
        'Walc': 5, 'health': 2, 'absences': 10, 'G1': 14, 'G2': 15, 'G3': 16, 
        'part_time_job': 'yes'
    }

    result = process_dict_to_array(counselor_input)
    print("Final Array for Predict.py:")
    print(result)
    print("Shape:", result.shape)
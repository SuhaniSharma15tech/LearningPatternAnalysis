
student_record = {
    "Hours_Studied": 23,
    "Attendance": 84,
    "Parental_Involvement": "Low",
    "Access_to_Resources": "High",
    "Extracurricular_Activities": "No",
    "Sleep_Hours": 7,
    "Previous_Scores": 73,
    "Motivation_Level": "Low",
    "Internet_Access": "Yes",
    "Tutoring_Sessions": 0,
    "Family_Income": "Low",
    "Teacher_Quality": "Medium",
    "School_Type": "Public",
    "Peer_Influence": "Positive",
    "Physical_Activity": 3,
    "Learning_Disabilities": "No",
    "Parental_Education_Level": "High School",
    "Distance_from_Home": "Near",
    "Gender": "Male",
    "Exam_Score": 67
}
def numerical_mapping(record):

        # Mapping definitions
        ordinal_map = {'Low': 0, 'Medium': 1, 'High': 2}
        binary_map = {'No': 0, 'Yes': 1}
        school_map = {'Public': 0, 'Private': 1}
        peer_map = {'Negative': 0, 'Neutral': 1, 'Positive': 2}
        edu_map = {'High School': 0, 'College': 1, 'Postgraduate': 2}
        dist_map = {'Near': 0, 'Moderate': 1, 'Far': 2}
        gender_map = {'Female': 0, 'Male': 1}

        # Column configuration
        mapping_dict = {
            'Parental_Involvement': ordinal_map,
            'Access_to_Resources': ordinal_map,
            'Motivation_Level': ordinal_map,
            'Family_Income': ordinal_map,
            'Teacher_Quality': ordinal_map,
            'Extracurricular_Activities': binary_map,
            'Internet_Access': binary_map,
            'Learning_Disabilities': binary_map,
            'School_Type': school_map,
            'Peer_Influence': peer_map,
            'Parental_Education_Level': edu_map,
            'Distance_from_Home': dist_map,
            'Gender': gender_map
            }

        # generate mapping
        for i in record.keys():
            if i in mapping_dict:
               record[i]=mapping_dict[i][record[i]]
            else:
                pass
        return(record)
print(numerical_mapping(student_record))
def reduce_single_scaled_record(scaled_record):
    """
    Reduces a single dictionary of 20 scaled features into 5 thematic scores.
    Assumes values in scaled_record are already scaled between 0 and 1.
    """
    # 1. Invert 'Negative' features (so 1.0 = Better for Success)
    # We use (1 - value) because the input is already scaled 0-1
    inverted_dist = 1.0 - scaled_record.get('Distance_from_Home', 0)
    inverted_disab = 1.0 - scaled_record.get('Learning_Disabilities', 0)

    # 2. Define Themes by averaging their respective components
    reduced_record = {}

    # Theme 1: Academic Drive (Effort & Motivation)
    reduced_record['Academic_Drive'] = sum([
        scaled_record['Hours_Studied'],
        scaled_record['Attendance'],
        scaled_record['Previous_Scores'],
        scaled_record['Motivation_Level']
    ]) / 4

    # Theme 2: Resource Access (Socio-economic & School Tools)
    reduced_record['Resource_Access'] = sum([
        scaled_record['Access_to_Resources'],
        scaled_record['Internet_Access'],
        scaled_record['Tutoring_Sessions'],
        scaled_record['Family_Income'],
        scaled_record['Teacher_Quality'],
        scaled_record['School_Type']
    ]) / 6

    # Theme 3: Family Capital (Home Support)
    reduced_record['Family_Capital'] = sum([
        scaled_record['Parental_Involvement'],
        scaled_record['Parental_Education_Level']
    ]) / 2

    # Theme 4: Personal Wellbeing (Lifestyle)
    reduced_record['Personal_Wellbeing'] = sum([
        scaled_record['Sleep_Hours'],
        scaled_record['Physical_Activity'],
        scaled_record['Extracurricular_Activities']
    ]) / 3

    # Theme 5: Environmental Stability (External Factors)
    # Note: Using the inverted values here
    reduced_record['Environmental_Stability'] = sum([
        scaled_record['Peer_Influence'],
        inverted_dist,
        inverted_disab
    ]) / 3

    # Optional: Keep Exam_Score if it exists in the record
    if 'Exam_Score' in scaled_record:
        reduced_record['Exam_Score'] = scaled_record['Exam_Score']

    return reduced_record
# print(reduce_single_scaled_record(numerical_mapping(student_record)))
# --- Example Usage ---
# scaled_input = {"Hours_Studied": 0.8, "Attendance": 0.9, ...} 
# thematic_output = reduce_single_scaled_record(scaled_input)
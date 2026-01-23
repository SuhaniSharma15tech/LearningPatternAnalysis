import csv

def process_and_export_data(input_file, output_file):
    # 1. Configuration: Mapping Dictionaries
    binary_map = {'yes': 1, 'no': 0, 'F': 1, 'M': 0, 'U': 1, 'R': 0, 
                  'GT3': 1, 'LE3': 0, 'T': 1, 'A': 0, 'GP': 1, 'MS': 0}
    
    job_map = {'teacher': 4, 'health': 3, 'services': 2, 'other': 1, 'at_home': 0}
    reason_map = {'reputation': 3, 'course': 2, 'home': 1, 'other': 0}
    guardian_map = {'mother': 2, 'father': 1, 'other': 0}
    
    bin_cols = ['school', 'sex', 'address', 'famsize', 'Pstatus', 'schoolsup', 
                'famsup', 'paid', 'activities', 'nursery', 'higher', 
                'internet', 'romantic', 'part_time_job']
    
    nominal_maps = {
        'Mjob': job_map, 
        'Fjob': job_map, 
        'reason': reason_map, 
        'guardian': guardian_map
    }

    # 2. Read, Transform, and Write
    with open(input_file, mode="r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        headers = reader.fieldnames
        
        with open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=headers)
            writer.writeheader()
            
            for row in reader:
                transformed_row = {}
                for col in headers:
                    val = row[col]
                    
                    # Apply Transformation Logic
                    if col in bin_cols:
                        transformed_row[col] = binary_map.get(val, val)
                    elif col in nominal_maps:
                        transformed_row[col] = nominal_maps[col].get(val, val)
                    else:
                        # Convert numeric strings to actual numbers (int or float)
                        try:
                            if '.' in val:
                                transformed_row[col] = float(val)
                            else:
                                transformed_row[col] = int(val)
                        except ValueError:
                            transformed_row[col] = val
                            
                writer.writerow(transformed_row)

# Execute the process
process_and_export_data("unprocessed.csv", "processed.csv")
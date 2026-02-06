from flask import Flask, jsonify, request , render_template
from utilities import analyze
app = Flask(__name__)

# homepage
@app.route('/')
def home():
    return render_template('index.html')

@app.route("/analyzeGroup", methods=["POST"])
def analyze_group():
    file = request.files["csv_file"]
    return jsonify(analyze.visualise(file)) 

    
@app.route("/analyzeStudent", methods=["POST"])
def analyze_student():
    # Convert  to  dictionary
    data = request.form.to_dict()
    
    # List of keys that should be numeric (int or float)
    numeric_keys = [
        "Hours_Studied", "Attendance", "Sleep_Hours", 
        "Previous_Scores", "Tutoring_Sessions", 
        "Physical_Activity", "Exam_Score"
    ]
    
    # Convert string inputs from form to floats
    for key in numeric_keys:
        if key in data and data[key]:
            try:
                # Using float() is safer than eval() for simple type conversion
                data[key] = float(data[key])
            except ValueError:
                # Fallback or error handling if input is not a number
                data[key] = 0.0

    return jsonify(analyze.visualise(data))


if __name__ == "__main__":
    app.run(debug=True)
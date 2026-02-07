import os
import requests
import json
from flask import Flask, jsonify, request, render_template
from utilities import analyze

app = Flask(__name__)

# CONFIGURATION: Set your API Key here or as an environment variable
GEMINI_API_KEY = "" # Leave empty for the runtime environment to provide it

def get_ai_insight(data_summary):
    """Calls Gemini API to generate professional teaching insights."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={GEMINI_API_KEY}"
    
    prompt = f"""
    As an AI Education Consultant, analyze this student data and provide 3-4 bullet points 
    of actionable 'Strategic Insights' for a teacher. Keep it professional, encouraging, 
    and focused on student success. 
    
    Data Context: {json.dumps(data_summary)}
    """
    
    payload = {
        "contents": [{ "parts": [{ "text": prompt }] }]
    }
    
    # Implementing retry logic with backoff
    for delay in [1, 2, 4, 8, 16]:
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
        except Exception:
            pass
    return "AI Insights are temporarily unavailable. Please try again later."

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/analyzeGroup", methods=["POST"])
def analyze_group():
    file = request.files["csv_file"]
    analysis_results = analyze.visualise(file)
    
    # Generate AI insights based on the analysis
    summary = {
        "type": "batch",
        "clusters": analysis_results['charts']['academic_distribution']
    }
    analysis_results['ai_insight'] = get_ai_insight(summary)
    
    return jsonify(analysis_results)

@app.route("/analyzeStudent", methods=["POST"])
def analyze_student():
    data = request.form.to_dict()
    numeric_keys = ["Hours_Studied", "Attendance", "Sleep_Hours", "Previous_Scores", "Tutoring_Sessions", "Physical_Activity"]
    
    for key in numeric_keys:
        if key in data and data[key]:
            try:
                data[key] = float(data[key])
            except ValueError:
                data[key] = 0.0

    analysis_results = analyze.visualise(data)
    
    # Generate AI insights for single student
    summary = {
        "type": "single",
        "predicted_score": analysis_results['score_value'],
        "metrics": analysis_results['charts']['spider_chart']['data']
    }
    analysis_results['ai_insight'] = get_ai_insight(summary)
    
    return jsonify(analysis_results)

if __name__ == "__main__":
    app.run(debug=True)
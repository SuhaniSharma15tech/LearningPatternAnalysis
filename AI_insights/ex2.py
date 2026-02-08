def get_ai_insight(data_summary):
    """Calls Gemini API to generate deep pedagogical insights based on student clustering and persona logic."""
    # Ensure we use the correct model for the environment
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={GEMINI_API_KEY}"
    
    # Comprehensive System Prompt for the Analyst
    system_context = """
    As an expert Educational Analyst, interpret student data based on these core frameworks:
    
    1. THEMATIC FEATURES:
       - Academic Drive (Hours, Attendance, Motivation)
       - Resource Access (Internet, Tutoring, School Quality)
       - Family Capital (Parental Involvement & Education)
       - Personal Wellbeing (Sleep, Activity)
       - Environmental Stability (Peer Influence, Distance, Disabilities)

    2. ACADEMIC CLUSTERS:
       - Improved: High/Rising trajectory.
       - Steady: Consistent but potentially plateaued.
       - Declining: Dropping performance; needs urgent intervention.

    3. PERSONA CLUSTERS: Define behavioral archetypes based on the 5 thematic feature centroids.

    4. SCENARIOS:
       - Scenario A: Predicting Score (Future outlook).
       - Scenario B: Actual Exam_Score analysis (Root cause analysis).
    """

    user_query = f"""
    Analyze this data summary: {json.dumps(data_summary)}

    REQUIRED OUTPUT FORMAT:
    If data type is 'single':
      1. Unique strengths, weaknesses, and struggles.
      2. Specific actionable help to increase their level.
      3. (If prediction) Analyze their academic future.

    If data type is 'batch':
      1. Academic composition analysis (using academic distribution).
      2. Persona composition analysis.
      3. Unique class needs and teaching strategy changes.
      4. Success factors for High Performers vs. roadblocks for Steady Performers.
      5. Comparison: Why are Steady performers different from Declining ones? What must be maintained?
      6. Root causes for the average 'Declining' student.
      7. Specific improvement roadmap for each academic cluster.
    """
    
    payload = {
        "contents": [{ "parts": [{ "text": user_query }] }],
        "systemInstruction": { "parts": [{ "text": system_context }] }
    }
    
    # Implementing exponential backoff
    for delay in [1, 2, 4, 8, 16]:
        try:
            response = requests.post(url, json=payload, timeout=15)
            if response.status_code == 200:
                result = response.json()
                # Use the correct path for the preview environment model
                return result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "Insight generation failed.")
            elif response.status_code == 429:
                import time
                time.sleep(delay)
                continue
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            import time
            time.sleep(delay)
            last_error = str(e)
            
    return f"Unable to reach analysis engine: {last_error}"

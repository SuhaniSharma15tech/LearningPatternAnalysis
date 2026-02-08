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
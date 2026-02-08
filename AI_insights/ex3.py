# -----------------AYUSHI SENT THIS
def get_ai_insight(data_summary):
    """
    AI Insights Engine: Converts raw student data into product-ready dashboard insights.
    Focuses on Detection -> Decision -> Action workflow.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key={GEMINI_API_KEY}"
    
    # SYSTEM PROMPT: Strict Hackathon Rules
    system_prompt = """
    You are an AI insights engine built for a hackathon education product.
    Your task is NOT to write long analysis.
    Your task is to convert student performance data into CLEAR, ACTIONABLE, PRODUCT-READY INSIGHTS.

    STRICT RULES:
    1. Always think in terms of a dashboard or automated system.
    2. Focus on DETECTION → DECISION → ACTION.
    3. Avoid academic, sociological, or philosophical language.
    4. Do NOT repeat percentages or restate the same idea.
    5. Output must be concise and readable by judges in under 30 seconds.

    OUTPUT FORMAT (MANDATORY):
    SECTION 1: CORE INSIGHT (max 2 lines)
    SECTION 2: SYSTEM DETECTION (bullet points)
    SECTION 3: AUTO-ACTIONS TRIGGERED (short bullets)
    SECTION 4: IMPACT (2-3 measurable outcomes)

    STYLE: Product/AI/Startup tone. No emotional language.
    """

    user_query = f"INPUT DATA: {json.dumps(data_summary)}"
    
    payload = {
        "contents": [{ "parts": [{ "text": user_query }] }],
        "systemInstruction": { "parts": [{ "text": system_prompt }] }
    }
    
    # Exponential backoff retry logic (5 attempts)
    for delay in [1, 2, 4, 8, 16]:
        try:
            response = requests.post(url, json=payload, timeout=15)
            if response.status_code == 200:
                result = response.json()
                return result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', "Insight generation failed.")
            elif response.status_code == 429:
                time.sleep(delay)
                continue
            else:
                return f"AI Engine Error: {response.status_code}"
        except Exception:
            time.sleep(delay)
            
    return "Insights are currently offline. Check system logs."

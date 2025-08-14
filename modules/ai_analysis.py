import os
import google.generativeai as genai

def _try_config():
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

def analyze_text_with_gemini(text, system_hint="Summarize and analyze this content for competitive insights."):
    if not _try_config():
        return "⚠️ GEMINI_API_KEY not set. Add it to your .env."
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"{system_hint}\n\n{text}"
    try:
        resp = model.generate_content(prompt)
        return resp.text.strip() if hasattr(resp, "text") else "No response."
    except Exception as e:
        return f"Gemini error: {e}"

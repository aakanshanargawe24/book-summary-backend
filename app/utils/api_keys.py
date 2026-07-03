from app.core.config import GEMINI_API_KEY



def get_gemini_api_key() -> str:
    if not GEMINI_API_KEY:
        raise ValueError("Gemini API Key not found.")

    return GEMINI_API_KEY
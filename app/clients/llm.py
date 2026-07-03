from google import genai

from app.utils.api_keys import get_gemini_api_key


class LLMClient:

    def __init__(self):
        self.gemini_client = genai.Client(
            api_key=get_gemini_api_key()
        )

    def generate_content(
        self,
        prompt: str,
        model: str = "gemini-2.5-flash"
    ) -> str:

        llm_response = self.gemini_client.models.generate_content(
            model=model,
            contents=prompt
        )

        return llm_response.text
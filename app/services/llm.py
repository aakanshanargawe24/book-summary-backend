
from google import genai

from app.utils.api_keys import get_gemini_api_key


class LLM:

    def __init__(self):
        self.client = genai.Client(
            api_key=get_gemini_api_key()
        )

    def generate(
        self,
        prompt: str,
        model: str = "gemini-2.5-flash"
    ) -> str:

        response = self.client.models.generate_content(
            model=model,
            contents=prompt
        )

        return response.text
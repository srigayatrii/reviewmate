import json
from google import genai

from app.ai.prompts import CODE_REVIEW_PROMPT
from app.core.config import settings


class AIClient:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    async def review_patch(
        self,
        patch: str
    ):
        prompt = CODE_REVIEW_PROMPT.format(
            patch=patch
        )

        response = self.client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        text = response.text.strip()
        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)

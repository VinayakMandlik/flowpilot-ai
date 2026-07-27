from typing import Generator

from google import genai
from google.genai.errors import ClientError

from app.core.config import settings
from app.providers.base_provider import BaseProvider


class GeminiProvider(BaseProvider):

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = settings.LLM_MODEL

    def stream(
        self,
        prompt: str,
    ) -> Generator[str, None, None]:

        try:

            response = self.client.models.generate_content_stream(
                model=self.model,
                contents=prompt,
            )

            for chunk in response:

                if chunk.text:
                    yield chunk.text

        except ClientError as e:

            error = str(e)

            if "RESOURCE_EXHAUSTED" in error:

                yield (
                    "⚠️ Gemini API quota exceeded. "
                    "Please try again later."
                )

            elif "API_KEY_INVALID" in error:

                yield (
                    "⚠️ Invalid Gemini API key."
                )

            else:

                yield (
                    f"⚠️ Gemini Error:\n{error}"
                )

        except TimeoutError:

            yield (
                "⚠️ Gemini request timed out."
            )

        except Exception as e:

            yield (
                f"⚠️ Unexpected Gemini Error:\n{str(e)}"
            )
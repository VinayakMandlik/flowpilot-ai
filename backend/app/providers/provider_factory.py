from app.core.config import settings

from app.providers.gemini_provider import GeminiProvider


class ProviderFactory:

    _providers = {
        "gemini": GeminiProvider,
    }

    @classmethod
    def get_provider(cls):

        provider = settings.LLM_PROVIDER.lower()

        if provider not in cls._providers:
            raise ValueError(
                f"Unsupported LLM Provider: {provider}"
            )

        return cls._providers[provider]()
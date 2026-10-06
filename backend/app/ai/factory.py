from app.core.config import settings
from app.ai.base import AIProvider
from app.ai.mock_provider import MockAIProvider


def get_ai_provider() -> AIProvider:
    # If OPENAI_API_KEY is supplied and USE_MOCK_AI is False, can use OpenAIProvider
    if settings.OPENAI_API_KEY and not settings.USE_MOCK_AI:
        try:
            from app.ai.openai_provider import OpenAIProvider
            return OpenAIProvider()
        except Exception:
            return MockAIProvider()
    return MockAIProvider()

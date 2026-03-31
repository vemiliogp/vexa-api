"""LLM service module."""

from dataclasses import dataclass

from litellm import completion

mapping = {
    "deepseek/r1": "deepseek/deepseek-chat",
    "openai/gpt-5": "openai/gpt-5",
    "openai/gpt-oss": "ollama_chat/gpt-oss:latest",
}


@dataclass
class LLMService:
    """Service for handling language model completions."""

    @staticmethod
    async def generate(message: str, model_key: str) -> str:
        """Generate a completion from the LLM."""

        try:
            model = mapping.get(model_key)
            response = completion(
                model=model,
                messages=[{"role": "user", "content": message}],
                api_base="http://localhost:11434" if "ollama" in model else None,
            )
            message = response.choices[0].message

            return message.content
        except Exception as e:
            raise e

"""LLM service module."""

from dataclasses import dataclass

from litellm import completion

mapping = {
    "deepseek/r1": "deepseek/deepseek-chat",
    "openai/gpt-5": "openai/gpt-5",
    "openai/gpt-oss": "ollama/gpt-oss",
}


@dataclass
class LLMService:
    """Service for handling language model completions."""

    async def generate(self, message: str, model_key: str) -> str:
        """Generate a completion from the LLM."""

        try:
            response = completion.create(
                model=mapping.get(model_key),
                messages=[{"role": "user", "content": message}],
            )
            message = response.choices[0].message

            return message
        except Exception as e:
            raise e

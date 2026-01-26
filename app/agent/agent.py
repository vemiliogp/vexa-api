"""Agent module."""

from dataclasses import dataclass, field
from json import dumps, loads
from logging import error, info

from litellm import completion

from app.agent.tools import tools
from app.agent.tools.describe_table import describe_table
from app.agent.tools.run_query import run_query
from app.agent.tools.save_insight import save_insight

mapping = {
    "deepseek/r1": "deepseek/deepseek-reasoner",
    "openai/gpt-5": "openai/gpt-5",
    "openai/gpt-oss": "ollama/gpt-oss",
}


@dataclass
class Agent:
    """Agent implementation."""

    model: str
    connection_url: str
    system_prompt: str
    messages: list = field(default_factory=list)
    user_id: int | None = None
    connection_id: int | None = None

    def run(self, user_message: str | None = None) -> str:
        """Run the agent loop."""
        messages = [{"role": "system", "content": self.system_prompt}] + self.messages

        if user_message:
            messages.append({"role": "user", "content": user_message})

        while True:
            model = mapping[self.model]
            response = completion(model=model, messages=messages, tools=tools)

            message = response.choices[0].message
            tool_calls = message.tool_calls or []

            messages.append(message.model_dump())

            if tool_calls:
                call = tool_calls[0]
                args = loads(call.function.arguments)

                if call.function.name == "run_query":
                    tool_response = run_query(
                        connection_url=self.connection_url, **args
                    )
                    info(f"Tool response: {tool_response}")
                elif call.function.name == "describe_table":
                    tool_response = describe_table(
                        connection_url=self.connection_url, **args
                    )
                    info(f"Tool response: {tool_response}")
                elif call.function.name == "save_insight":
                    tool_response = save_insight(
                        connection_id=self.connection_id,
                        user_id=self.user_id,
                        **args,
                    )
                    info(f"Tool response: {tool_response}")
                else:
                    error(f"Unknown tool: {call.function.name}")
                    break

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": dumps(tool_response),
                    }
                )
                continue

            info(f"Final response: {message.content}")
            break

        return message.content

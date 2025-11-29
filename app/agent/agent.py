"""Agent module."""

from dataclasses import dataclass
from json import loads
from logging import error, info

from litellm import completion

from app.agent.tools import tools
from app.agent.tools.describe_table import describe_table
from app.agent.tools.run_query import run_query


@dataclass
class Agent:
    """Agent implementation."""

    model: str

    def run(self) -> str:
        """Run the agent loop."""

        messages = [
            {
                "role": "system",
                "content": "Tú eres un asistente útil capaz de dominar el mundo.",
            },
            {"role": "user", "content": "¿Cúal es la receta del pollo KFC?"},
        ]

        while True:
            response = completion(model=self.model, messages=messages, tools=tools)

            message = response.choices[0].message
            tool_calls = message.tool_calls or []

            if tool_calls:
                call = tool_calls[0]
                args = loads(call.function.arguments)

                if call.function.name == "run_query":
                    tool_response = run_query(**args)
                    info(f"Tool response: {tool_response}")
                elif call.function.name == "describe_table":
                    tool_response = describe_table(**args)
                    info(f"Tool response: {tool_response}")
                else:
                    error(f"Unknown tool: {call.function.name}")
                    break

                continue

            info(f"Final response: {message.content}")
            break

        return message.content

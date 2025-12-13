"""Agent module."""

from dataclasses import dataclass
from json import dumps, loads
from logging import error, info

from litellm import completion

from app.agent.tools import tools
from app.agent.tools.describe_table import describe_table
from app.agent.tools.run_query import run_query


@dataclass
class Agent:
    """Agent implementation."""

    model: str
    connection_url: str

    def run(self, message: str) -> str:
        """Run the agent loop."""

        messages = [
            {
                "role": "system",
                "content": """
                    Tu eres un asistente, esta son las tablas que tienes en tu base de datos:
                    actor,store,address,category,city,country,customer,film_actor,film_category,inventory,language,rental,staff,payment,film
                    Si tienes duda utiliza las tools correspondientes para inspeccionar dentro de cada una
                """,
            },
            {"role": "user", "content": message},
        ]

        while True:
            response = completion(model=self.model, messages=messages, tools=tools)

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

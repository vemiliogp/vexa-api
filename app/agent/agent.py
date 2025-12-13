"""Agent module."""

from dataclasses import dataclass
from json import dumps, loads
from logging import error, info

from litellm import completion

from app.agent.tools import tools
from app.agent.tools.describe_table import describe_table
from app.agent.tools.run_query import run_query
from app.services.database import DatabaseService

mapping = {
    "deepseek-r1": "deepseek/deepseek-reasoner",
    "openai/gpt-4o": "openai/gpt-4o",
    "ollama/gtp-oss": "ollama/gpt-oss",
}


@dataclass
class Agent:
    """Agent implementation."""

    model: str
    connection_url: str
    messages: list

    def run(self, message: str) -> str:
        """Run the agent loop."""

        self.messages.append(
            {
                "role": "system",
                "content": f"""Eres un asistente de bases de datos SQL.
                    Tablas disponibles en la base de datos:
                    {', '.join(DatabaseService.get_tables(self.connection_url))}

                    Instrucciones:
                    - Construye consultas SQL precisas basándote en las preguntas del usuario
                    - Si no estás seguro de algo, inspecciona primero la tabla antes de consultar

                    Responde de forma clara y concisa (solo texto, sin markdown).""",
            }
        )
        self.messages.append({"role": "user", "content": message})

        while True:
            print(self.messages)
            model = mapping[self.model]
            response = completion(model=model, messages=self.messages, tools=tools)

            message = response.choices[0].message
            tool_calls = message.tool_calls or []

            self.messages.append(message.model_dump())

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

                self.messages.append(
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

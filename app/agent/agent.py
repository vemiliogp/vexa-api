"""Agent module."""

from dataclasses import dataclass
from json import dumps, loads
from logging import error, info

from litellm import completion

from app.agent.tools import tools
from app.agent.tools.describe_table import describe_table
from app.agent.tools.run_query import run_query

mapping = {
    "deepseek/r1": "deepseek/deepseek-chat",
    "openai/gpt-5": "openai/gpt-5",
    "openai/gpt-oss": "ollama/gpt-oss",
}


@dataclass
class Agent:
    """Agent implementation."""

    model: str
    connection_url: str
    messages: list
    context: str
    tables: str

    def run(self, message: str) -> str:
        """Run the agent loop."""
        self.messages.insert(
            0,
            {
                "role": "system",
                "content": f"""
                    Eres un agente experto en análisis de datos y consultas SQL. Tu función principal es ayudar a los usuarios a explorar y analizar la base de datos.

                    <available_tables>
                    Las siguientes tablas están disponibles para consulta:
                    {self.tables}
                    </available_tables>

                    <business_context>
                    {self.context}
                    </business_context>

                    <core_principles>

                    <no_fabrication>
                    NUNCA inventes datos, estructuras de tablas o resultados.
                    - Ante cualquier duda sobre la estructura de una tabla, usa las herramientas disponibles para inspeccionarla
                    - Si no estás seguro de que una columna existe, verifica primero
                    - Si una consulta falla, analiza el error antes de intentar otra solución
                    - Prefiere siempre verificar con herramientas antes de asumir
                    </no_fabrication>

                    <tools_first>
                    Antes de responder cualquier pregunta sobre los datos:
                    1. Usa las herramientas para explorar la estructura de las tablas relevantes
                    2. Verifica que las columnas que planeas usar existen
                    3. Ejecuta la consulta para obtener resultados reales
                    4. Solo entonces proporciona tu análisis basado en datos concretos
                    </tools_first>

                    <query_restrictions>
                    RESTRICCIONES CRÍTICAS DE SEGURIDAD:
                    - SOLO puedes ejecutar sentencias SELECT
                    - PROHIBIDO: INSERT, UPDATE, DELETE, DROP, CREATE, ALTER, TRUNCATE, GRANT, REVOKE
                    - PROHIBIDO: Cualquier sentencia que modifique datos o estructura
                    - Si el usuario solicita modificar datos, explica que solo tienes permisos de lectura
                    </query_restrictions>

                    <no_tables_behavior>
                    Si no hay tablas disponibles en <available_tables>:
                    - Informa claramente al usuario que no hay datos para explorar
                    - No intentes ejecutar consultas
                    - Sugiere verificar la conexión a la base de datos o contactar al administrador
                    </no_tables_behavior>

                    </core_principles>

                    <query_refinement>
                    Antes de ejecutar una consulta, refina la pregunta del usuario:

                    1. Clarifica la intención: ¿Qué información específica necesita el usuario?
                    2. Identifica las tablas: ¿Qué tablas son relevantes para responder?
                    3. Define filtros: ¿Hay condiciones temporales, de categoría u otras?
                    4. Determina agregaciones: ¿Necesita totales, promedios, conteos?

                    Transforma preguntas vagas en consultas específicas antes de ejecutar.
                    </query_refinement>

                    <output_format>
                    IMPORTANTE: Todas tus respuestas deben ser texto plano.
                    - NO uses markdown (ni asteriscos, ni almohadillas, ni backticks)
                    - NO uses formato de código
                    - No uses saltos de lineas, la respuesta debe ser un párrafo continuo
                    - NO uses negritas, cursivas ni encabezados
                    - NO uses listas con viñetas ni numeradas con formato especial
                    - Presenta la información de forma clara usando solo texto simple
                    </output_format>

                    <best_practices>
                    - Usa alias claros para columnas y tablas
                    - Limita los resultados cuando sea apropiado (LIMIT)
                    - Ordena los resultados de manera lógica
                    - Maneja valores NULL apropiadamente
                    - Usa JOINs cuando sea necesario para relacionar tablas
                    - Explica tu razonamiento al construir consultas complejas
                    </best_practices>
                """,
            },
        )
        self.messages.append({"role": "user", "content": message})

        while True:
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

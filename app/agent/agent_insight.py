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
class AgentInsight:
    """Agent implementation."""

    model: str
    connection_url: str
    context: str
    tables: str

    def run(self, num_insights: int) -> str:
        """Run the agent loop."""
        messages = []
        messages.insert(
            0,
            {
                "role": "system",
                "content": f"""
                    Eres un agente experto en descubrimiento de insights y análisis exploratorio de datos. Tu función principal es investigar proactivamente la base de datos para encontrar patrones, anomalías y hallazgos valiosos sin esperar preguntas específicas del usuario.

                    <available_tables>
                    Las siguientes tablas están disponibles para exploración:
                    {self.tables}
                    </available_tables>

                    <business_context>
                    {self.context}
                    </business_context>

                    <exploration_goal>
                    Debes encontrar exactamente {num_insights} insights relevantes y accionables.
                    </exploration_goal>

                    <core_principles>

                    <proactive_exploration>
                    Tu trabajo es BUSCAR activamente, no esperar instrucciones:
                    - Explora todas las tablas disponibles sistemáticamente
                    - Cruza datos entre tablas para encontrar correlaciones
                    - Busca valores atípicos, tendencias y patrones ocultos
                    - Compara períodos, categorías y segmentos
                    - Identifica oportunidades y riesgos en los datos
                    </proactive_exploration>

                    <no_fabrication>
                    NUNCA inventes datos ni resultados.
                    - Usa siempre las herramientas para obtener datos reales antes de reportar un insight
                    - Si una consulta falla, intenta otra aproximación
                    - Solo reporta hallazgos respaldados por datos concretos
                    - Incluye los números exactos que sustentan cada insight
                    </no_fabrication>

                    <tools_first>
                    Para cada insight:
                    1. Primero explora la estructura de las tablas relevantes
                    2. Ejecuta consultas para obtener datos reales
                    3. Valida el hallazgo con los números obtenidos
                    4. Solo entonces repórtalo como insight
                    </tools_first>

                    <query_restrictions>
                    RESTRICCIONES DE SEGURIDAD:
                    - SOLO puedes ejecutar sentencias SELECT
                    - PROHIBIDO: INSERT, UPDATE, DELETE, DROP, CREATE, ALTER, TRUNCATE, GRANT, REVOKE
                    </query_restrictions>

                    <no_tables_behavior>
                    Si no hay tablas disponibles:
                    - Informa que no hay datos para explorar
                    - No intentes ejecutar consultas
                    </no_tables_behavior>

                    </core_principles>

                    <exploration_strategies>
                    Aplica estas estrategias para descubrir insights:

                    1. Distribuciones: Analiza cómo se distribuyen los valores en columnas clave
                    2. Tendencias temporales: Busca cambios a lo largo del tiempo si hay fechas disponibles
                    3. Comparaciones: Compara segmentos, categorías o grupos entre sí
                    4. Anomalías: Identifica valores extremos, outliers o registros inusuales
                    5. Correlaciones: Busca relaciones entre diferentes métricas o dimensiones
                    6. Rankings: Encuentra los top y bottom performers en diferentes métricas
                    7. Concentraciones: Detecta si pocos elementos concentran la mayoría del valor
                    8. Brechas: Identifica diferencias significativas entre grupos o períodos
                    9. Patrones cíclicos: Busca comportamientos repetitivos en los datos
                    10. Datos faltantes: Detecta problemas de calidad o registros incompletos
                    </exploration_strategies>

                    <insight_quality>
                    Cada insight debe ser:
                    - Específico: Con números concretos, no generalidades
                    - Relevante: Útil para la toma de decisiones según el contexto de negocio
                    - Accionable: Que sugiera una posible acción o investigación adicional
                    - Verificable: Basado en datos que se pueden consultar
                    - No obvio: Que aporte información que no sea evidente a simple vista
                    </insight_quality>

                    <output_format>
                    IMPORTANTE: Tu respuesta debe ser texto plano sin formato.
                    - NO uses markdown, asteriscos, almohadillas ni backticks
                    - NO uses negritas, cursivas ni encabezados
                    - NO uses listas con viñetas ni numeradas
                    - NO uses saltos de línea innecesarios
                    - Presenta los insights como un párrafo continuo, separando cada insight con un punto y seguido
                    - Incluye los datos numéricos que respaldan cada hallazgo dentro del texto
                    </output_format>

                    <execution_flow>
                    1. Explora primero la estructura de todas las tablas disponibles
                    2. Identifica las columnas más relevantes según el contexto de negocio
                    3. Ejecuta consultas exploratorias para entender los datos
                    4. Profundiza en áreas donde detectes patrones interesantes
                    5. Valida cada hallazgo con consultas adicionales si es necesario
                    6. Reporta exactamente {num_insights} insights con sus datos de respaldo
                    </execution_flow>
                """,
            },
        )

        while True:
            model = mapping[self.model]
            response = completion(model=model, messages=messages, tools=tools)

            message = response.choices[0].message
            tool_calls = message.tool_calls or []
            
            print(message)

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

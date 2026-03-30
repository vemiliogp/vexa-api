# REST API

Servicio backend construido con **Python 3.12**, **FastAPI** y **Tortoise ORM**. Expone endpoints para autenticación, conversaciones, conexiones, insights y un agente de IA con herramientas (tool-calling). Incluye speech-to-text (Whisper), text-to-speech (Edge TTS), almacenamiento de objetos (MinIO) y seguimiento de experimentos (MLflow).

## Requisitos

- [Python 3.12.12+](https://www.python.org/)
- [uv](https://github.com/astral-sh/uv) (recomendado) o pip 24+
- [Docker](https://www.docker.com/) y Docker Compose
- [Ollama](https://ollama.com/) (necesario para el modelo LLM local)
- `openssl` (para generar secrets seguros)

## Instalación

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/vemiliogp/vexa-api.git
   cd vexa-api
   ```

2. **Instalar dependencias:**

   Con **uv** (recomendado):

   ```bash
   uv sync
   ```

   O con `pip` dentro de un entorno virtual:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno:**

   ```bash
   cp .env.example .env
   ```

   Abrí el archivo `.env` y configurá las variables necesarias.

4. **Generar secrets para las variables de entorno:**

   Ejecutá el siguiente comando para generar secrets únicos:

   ```bash
   openssl rand -base64 32
   ```

   Repetí según sea necesario para `DB_PASSWORD`, `SESSION_SECRET`, `ENCRYPT_SECRET` y `MINIO_ROOT_PASSWORD`. Por ejemplo:

   ```bash
   DB_PASSWORD=""
   SESSION_SECRET=""
   ```

5. **Configurar credenciales de Docker en `.env.docker`:**

   El archivo `.env.docker` contiene las credenciales que usan los contenedores de Docker Compose (PostgreSQL y MinIO). Crealo con las mismas credenciales que definiste en `.env`:

   ```bash
   # Database configuration
   DB_USER=vexa_user
   DB_PASSWORD=<tu_db_password>
   DB_NAME=vexa_db

   # Storage service configuration
   MINIO_ROOT_USER=vexa
   MINIO_ROOT_PASSWORD=<tu_minio_password>
   EOF
   ```

   Los valores de `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `MINIO_ROOT_USER` y `MINIO_ROOT_PASSWORD` deben coincidir con los de tu archivo `.env` para que la API pueda conectarse correctamente a los servicios.

6. **Instalar y configurar Ollama:**

   Instalá Ollama siguiendo las instrucciones en [ollama.com](https://ollama.com/) y descargá el modelo local:

   ```bash
   ollama pull gpt-oss:20b

   Asegurate de que Ollama esté corriendo antes de iniciar la API si vas a usar el modelo `openai/gpt-oss`:

   ```bash
   ollama serve
   ```

7. **Iniciar los servicios de infraestructura:**

   ```bash
   docker compose up -d db storage
   ```

   Esto levanta PostgreSQL y MinIO. El directorio local `postgresql/` se monta como volumen para que los datos persistan entre ejecuciones. La consola de MinIO está disponible en `http://localhost:9001`.

8. **Iniciar el servidor de MLflow:**

   ```bash
   uv run mlflow server --port 7500
   ```

   > **Importante:** El servidor de MLflow debe estar corriendo antes de iniciar la API. Sin él, la aplicación no arrancará porque intenta conectarse a MLflow al inicio.

   Una vez levantado, la interfaz web de MLflow está disponible en `http://localhost:7500`. Asegurate de que la variable `MLFLOW_TRACKING_URI` en tu `.env` apunte a esta dirección.

## Ejecución

### Servidor de desarrollo local

```bash
uv run fastapi dev app/main.py
```

Este comando carga las variables de entorno desde `.env`, crea la app de FastAPI y Tortoise crea automáticamente las tablas definidas en `app.models`.

### Docker Compose (stack completo)

```bash
docker compose up --build
```

El servicio `api` usa el Dockerfile en la raíz del proyecto y se conecta a los servicios `db` y `storage` definidos en `compose.yaml`.

## Comandos disponibles

- `uv run fastapi dev app/main.py` – Ejecutar la API en modo desarrollo con auto-reload.
- `uv run fastapi run app/main.py` – Ejecutar la API en modo producción.

## Estructura del proyecto

```plaintext
app/                         # Paquete de la aplicación FastAPI
  main.py                    # Punto de entrada, configuración de FastAPI + Tortoise
  agent/                     # Agente de IA con capacidades de tool-calling
    agent.py                 # Implementación del loop del agente
    prompts/                 # Prompts de sistema para el agente
    tools/                   # Herramientas del agente (run_query, describe_table, save_insight)
  config/                    # Configuración de la app (base de datos, middlewares, lifespan)
  controllers/               # Controladores HTTP que orquestan los servicios
  dtos/                      # Modelos para request/response bodies
  exceptions/                # Manejo de errores y definiciones personalizadas
  middlewares/               # Funciones middleware para procesamiento de requests
  models/                    # Modelos Tortoise ORM (User, Connection, Conversation, Insight, Message)
  routes/                    # Instancias de APIRouter (auth, health, connection, conversation, insight)
  services/                  # Lógica de negocio (auth, LLM, transcripción, TTS, storage, email)
  utils/                     # Utilidades auxiliares
docs/                        # Documentación del proyecto
  er-diagram.png             # Diagrama entidad-relación
compose.yaml                 # Stack Docker Compose (API, PostgreSQL, MinIO)
Dockerfile                   # Imagen de contenedor para el servicio FastAPI
pyproject.toml               # Metadatos del proyecto y dependencias
requirements.txt             # Lista de dependencias bloqueada exportada por uv
uv.lock                      # Lockfile de uv para instalaciones reproducibles
.env.example                 # Plantilla de variables de entorno
```

## Documentación de la API

FastAPI genera documentación interactiva automáticamente en `http://localhost:8000/docs` una vez que el servicio está corriendo. Usá el endpoint `/health` para verificar que la API esté activa.

## Licencia

Este proyecto está licenciado bajo los términos de la Licencia ISC.

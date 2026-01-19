# LLM Gateway Microservice – Specs

## Objetivo

Microservicio HTTP que actúa como **gateway único de LLM** para múltiples proyectos internos.  
Los clientes llaman a este servicio; el servicio se comunica con la infraestructura remota de OllamaFreeAPI y, en el futuro, podrá cambiar de backend sin afectar a los clientes.

---

## Alcance inicial (MVP)

- Exponer endpoints unificados para:
  - Chat sin streaming.
  - Chat con streaming.
  - Listado de modelos disponibles.
- Gestionar proyectos/tenants mediante API keys.
- Registrar logs básicos de uso (por proyecto, modelo y timestamp).
- Proveer una base para un dashboard administrativo (no obligatorio en el primer commit).

---

## Stack técnico

- Lenguaje: **Python 3.11+**
- Framework web: **FastAPI** + Uvicorn/Gunicorn.
- Cliente LLM: **`ollamafreeapi`** (PyPI).
- Base de datos: PostgreSQL (con SQLAlchemy / SQLModel o equivalente).
- Autenticación para clientes: API key por proyecto (header: `X-API-Key`).
- Infraestructura objetivo: VPS con Docker + reverse proxy (Nginx/Traefik) para TLS.

---

## Modelo de dominio (v1)

### Project

- `id` (UUID)
- `name` (string)
- `description` (string, opcional)
- `api_key` (string, único, secreto)
- `is_active` (bool)
- `rate_limit_per_minute` (int, opcional)
- `allowed_models` (lista/JSON de nombres de modelo lógicos o físicos)

### RequestLog

- `id` (UUID)
- `project_id` (FK Project)
- `timestamp` (datetime)
- `model` (string, modelo físico usado, p.ej. `llama3.3:70b`)
- `endpoint` (string, p.ej. `/v1/chat`)
- `latency_ms` (int)
- `status` (int HTTP)
- `tokens_input` (int, opcional; estimado)
- `tokens_output` (int, opcional; estimado)

### ModelExposure (opcional v1, se puede derivar de `allowed_models`)

- `id`
- `project_id`
- `logical_name` (p.ej. `law-assistant`)
- `backend_model` (p.ej. `llama3:8b-instruct`)
- `config` (JSON de parámetros por defecto: temperatura, max_tokens, etc.)

---

## Contrato de API (público para proyectos)

### Autenticación

- Header obligatorio: `X-API-Key: <project_api_key>`.
- Respuestas:
  - 401 si falta o es inválida.
  - 403 si el proyecto está desactivado.

### `POST /v1/chat`

Chat sin streaming contra un modelo.

**Request body**

```json
{
  "model": "law-assistant",
  "messages": [
    { "role": "system", "content": "You are a helpful assistant." },
    { "role": "user", "content": "Pregunta del usuario..." }
  ],
  "temperature": 0.7,
  "max_tokens": 1024,
  "metadata": {
    "project_context": "optional",
    "correlation_id": "uuid-externo"
  }
}
```

- `model`: nombre lógico que el microservicio mapeará a un modelo físico de OllamaFreeAPI (`llama3.3:70b`, `deepseek-r1:7b`, etc.).
- `messages`: estilo OpenAI chat.
- `temperature`, `max_tokens`: overrides opcionales de la configuración por defecto del modelo.

**Response body (200)**

```json
{
  "id": "uuid-interno",
  "model": "llama3.3:70b",
  "object": "chat.completion",
  "created": 1737260000,
  "choices": [
    {
      "index": 0,
      "message": { "role": "assistant", "content": "Respuesta..." },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 123,
    "completion_tokens": 456,
    "total_tokens": 579
  }
}
```

### `POST /v1/chat/stream`

Chat con streaming (SSE o chunked JSON).

- Mismo body que `/v1/chat`.
- Respuesta: stream de eventos con fragmentos del contenido.
- Protocolo a definir según facilidad (SSE recomendado).

### `GET /v1/models`

Devuelve los modelos lógicos expuestos para ese proyecto.

**Response body**

```json
{
  "data": [
    {
      "name": "law-assistant",
      "backend_model": "llama3:8b-instruct",
      "description": "Modelo optimizado para consultas jurídicas.",
      "default_params": {
        "temperature": 0.2,
        "max_tokens": 1500
      }
    }
  ]
}
```

### `GET /v1/health`

- Devuelve estado simple del servicio.
- Opcionalmente, puede consultar un modelo ligero de OllamaFreeAPI o su endpoint de estado para health más profundo.

---

## Integración con OllamaFreeAPI

### Cliente

- Uso del cliente oficial `ollamafreeapi`:

  - Chat sin streaming: `client.chat(model_name, prompt, temperature, ...)`.
  - Chat streaming: `client.stream_chat(model_name, prompt, ...)`.
  - Modelos: `client.list_models()`, `client.get_model_info(name)`.

### Mapeo modelo lógico → modelo físico

- Tabla/config `ModelExposure` o campo `allowed_models` en `Project`.
- Cada modelo lógico define:
  - `backend_model`: nombre físico en OllamaFreeAPI.
  - Parámetros por defecto (temperature, max_tokens, etc.).

---

## Dashboard (v1 – lineamientos)

No bloquea el MVP, pero se diseña pensando en:

- Panel de administración interno en `/admin` (auth separada).
- Funcionalidades clave:
  - CRUD de proyectos (Project + API keys).
  - Visualización de logs básicos (RequestLog) por proyecto/modelo.
  - Vista de modelos disponibles en OllamaFreeAPI y su mapeo a modelos lógicos.
- Posibles stacks:
  - Fase 1: FastAPI + templates + librería de admin (FastAPI Admin / CRUDAdmin).
  - Fase 2: Dashboard React/Next.js independiente consumiendo la API admin.

---

## No objetivos (por ahora)

- No se gestionan embeddings ni file uploads.
- No se implementan aún workflows de agentes ni LangChain/LangGraph.
- No se hace RAG completo; solo passthrough + mínima lógica de negocio por proyecto.

---

## Roadmap siguiente

1. Crear estructura básica del proyecto (FastAPI + DB + modelos de dominio).
2. Implementar `Project` + auth por API key.
3. Implementar `/v1/chat` sobre OllamaFreeAPI con logging.
4. Implementar `/v1/models` con mapeo lógico → físico.
5. Añadir métrica simple (latencia, conteo por proyecto).
6. Diseñar endpoints internos para dashboard admin.

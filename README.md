# llm-gateway-service
Microservicio FastAPI que actúa como gateway unificado de LLM hacia OllamaFreeAPI para múltiples proyectos internos.

## 🎯 Descripción

Gateway HTTP centralizado para consumir modelos LLM desde múltiples proyectos internos. El servicio gestiona:

- **Autenticación** por API key (multi-tenant)
- **Proxy inteligente** hacia [OllamaFreeAPI](https://github.com/mfoud444/ollamafreeapi)
- **Mapeo de modelos** lógicos a modelos físicos
- **Logging y métricas** por proyecto
- **Base para dashboard** administrativo

## 📚 Documentación

- **[SPECS.md](./SPECS.md)**: Especificaciones completas del proyecto
- Stack: Python 3.11+, FastAPI, PostgreSQL, OllamaFreeAPI
- Arquitectura: Multi-tenant con API keys

## 🚀 Quick Start (Desarrollo Local)

### Prerrequisitos

- Python 3.11+
- PostgreSQL
- Git

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/Evincere/llm-gateway-service.git
cd llm-gateway-service

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\\Scripts\\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Ejecutar migraciones
alembic upgrade head

# Iniciar servidor de desarrollo
uvicorn app.main:app --reload
```

El servicio estará disponible en `http://localhost:8000`

## 💻 API Endpoints

### Autenticación

Todas las requests requieren el header:
```
X-API-Key: <tu_api_key>
```

### Endpoints principales

- `POST /v1/chat` - Chat sin streaming
- `POST /v1/chat/stream` - Chat con streaming (SSE)
- `GET /v1/models` - Lista modelos disponibles para tu proyecto
- `GET /v1/health` - Health check del servicio

### Ejemplo de uso

```bash
curl -X POST http://localhost:8000/v1/chat \\
  -H "X-API-Key: tu_api_key" \\
  -H "Content-Type: application/json" \\
  -d '{
    "model": "law-assistant",
    "messages": [
      {"role": "user", "content": "Hola, ¿cómo estás?"}
    ]
  }'
```

## 🛠️ Roadmap

- [x] Crear repositorio y especificaciones
- [ ] Implementar modelos de dominio (Project, RequestLog)
- [ ] Implementar autenticación por API key
- [ ] Endpoint `/v1/chat` con integración OllamaFreeAPI
- [ ] Endpoint `/v1/models`
- [ ] Sistema de logging
- [ ] Dashboard administrativo (fase 2)

## 📝 Licencia

MIT License - Ver [LICENSE](./LICENSE) para más detalles.

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.core.domain.project import Project

def test_health_check(client: TestClient):
    response = client.get("/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_chat_endpoint_requires_auth(client: TestClient):
    response = client.post("/v1/chat", json={"model": "test", "messages": []})
    assert response.status_code == 401
    assert "Missing API Key" in response.json()["detail"]

def test_chat_endpoint_valid_auth(client: TestClient, mock_project: Project):
    # Mock the LLM adapter to avoid real network calls
    with patch("app.entrypoints.api.chat_router.OllamaFreeAPIAdapter") as mock_adapter_class:
        mock_adapter = mock_adapter_class.return_value
        mock_adapter.chat.return_value = {"choices": [{"message": {"content": "response"}}]}
        
        response = client.post(
            "/v1/chat",
            json={"model": "llama3", "messages": [{"role": "user", "content": "hi"}]},
            headers={"X-API-Key": mock_project.api_key}
        )
        
        assert response.status_code == 200
        assert response.json()["choices"][0]["message"]["content"] == "response"

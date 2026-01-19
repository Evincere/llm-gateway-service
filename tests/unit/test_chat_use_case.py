import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from app.core.use_cases.chat import ChatWithModelUseCase
from app.core.domain.model_exposure import ModelExposure

def test_chat_use_case_with_mapped_model():
    # Arrange
    project_id = uuid4()
    logical_name = "law-assistant"
    backend_model = "llama3"
    messages = [{"role": "user", "content": "hello"}]
    
    mock_llm = MagicMock()
    mock_llm.chat.return_value = {"message": "hi"}
    
    mock_exposure_repo = MagicMock()
    mock_exposure_repo.get_by_logical_name.return_value = ModelExposure(
        project_id=project_id,
        logical_name=logical_name,
        backend_model=backend_model,
        config={"temperature": 0.1}
    )
    
    mock_log_repo = MagicMock()
    
    use_case = ChatWithModelUseCase(mock_llm, mock_exposure_repo, mock_log_repo)
    
    # Act
    response = use_case.execute(project_id, logical_name, messages)
    
    # Assert
    assert response == {"message": "hi"}
    mock_llm.chat.assert_called_once_with(
        model=backend_model, 
        messages=messages, 
        temperature=0.1
    )
    mock_log_repo.save.assert_called_once()

def test_chat_use_case_fallback_when_no_mapping():
    # Arrange
    project_id = uuid4()
    logical_name = "direct-model"
    messages = [{"role": "user", "content": "hello"}]
    
    mock_llm = MagicMock()
    mock_exposure_repo = MagicMock()
    mock_exposure_repo.get_by_logical_name.return_value = None
    mock_log_repo = MagicMock()
    
    use_case = ChatWithModelUseCase(mock_llm, mock_exposure_repo, mock_log_repo)
    
    # Act
    use_case.execute(project_id, logical_name, messages, top_p=0.9)
    
    # Assert
    mock_llm.chat.assert_called_once_with(
        model=logical_name, 
        messages=messages, 
        top_p=0.9
    )

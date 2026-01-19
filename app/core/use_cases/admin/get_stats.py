from typing import Dict, Any
from app.core.ports.repositories import LogRepository

class GetSystemStatsUseCase:
    """
    Use case for retrieving global usage statistics for administrators.
    """
    def __init__(self, log_repo: LogRepository):
        self.log_repo = log_repo

    def execute(self) -> Dict[str, Any]:
        # Orchestrate stats retrieval
        stats = self.log_repo.get_global_stats()
        
        # In the future, we could add more complex business logic or 
        # external monitoring data here.
        
        return stats

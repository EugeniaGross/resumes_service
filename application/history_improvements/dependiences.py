from history_improvements.repositories import (
    ResumeImprovementHistoryPostgreSQLRepository,
)
from history_improvements.services import ResumeImprovementHistoryService


def history_improvement_resume_service():
    return ResumeImprovementHistoryService(
        ResumeImprovementHistoryPostgreSQLRepository,
    )

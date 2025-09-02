from history_improvements.repositories import ResumeImprovementHistoryAbstractRepository
from history_improvements.models import ResumeImprovementHistory


class ResumeImprovementHistoryService:
    """
    Сервис для работы с историей улучшений резюме.
    Инкапсулирует бизнес-логику:
    - добавление истории улучшения резюме.

    Внешние зависимости: ResumesAbstractRepository.
    """

    def __init__(self, repo: ResumeImprovementHistoryAbstractRepository):
        """
        Инициализация сервиса резюме.

        Args:
            repo (ResumeImprovementHistoryAbstractRepository): Репозиторий для работы
                с БД.
        """
        self.repo: ResumeImprovementHistoryAbstractRepository = repo

    async def add_one(
        self, resume_id: int, improved_text: str
    ) -> ResumeImprovementHistory:
        """
        Добавляет запись об улучшении резюме.
        Args:
            resume_id (int): Идентификатор резюме.
            improved_text (str): Текст улучшенного резюме.
        Returns:
            ResumeHistory: Созданная запись.
        """
        return await self.repo.add_one(resume_id, improved_text)

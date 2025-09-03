from datetime import timezone, datetime
from typing import List
from zoneinfo import ZoneInfo

from history_improvements.repositories import ResumeImprovementHistoryAbstractRepository
from history_improvements.models import ResumeImprovementHistory
from resumes.services import ResumeService
from resumes.models import Resume


class ResumeImprovementHistoryService:
    """
    Сервис для работы с историей улучшений резюме.
    Инкапсулирует бизнес-логику:
    - добавление истории улучшения резюме.

    Внешние зависимости: ResumesAbstractRepository.
    """

    def __init__(
        self, 
        repo: ResumeImprovementHistoryAbstractRepository,
    ):
        """
        Инициализация сервиса истории улучшений резюме.

        Args:
            repo (ResumeImprovementHistoryAbstractRepository): Репозиторий для работы
                с БД.
        """
        self.repo: ResumeImprovementHistoryAbstractRepository = repo

    async def add_one(
        self, resume_id: int, improve_content: str, time_zone: str
    ) -> ResumeImprovementHistory:
        """
        Изменяет резюме и добавляет запись об улучшении резюме.
        Args:
            resume_id (int): Идентификатор резюме.
            improve_content (str): Текст улучшенного резюме.
            time_zone (str): Часовой пояс
        Returns:
            ResumeHistory: Созданная запись.
        """
        history = await self.repo.add_one(resume_id, improve_content)
        history.created_at = self.__update_timezone(history, time_zone)
        return history
    
    async def get_all_by_resume_id(self, resume_id: int, time_zone: str) -> List[ResumeImprovementHistory]:
        """
        Получает список всех улучшений резюме.
        Args:
            resume_id (int): Идентификатор резюме.
            time_zone (str): Часовой пояс
        Returns:
            List[ResumeImprovementHistory]: Список улучшений.
        """
        history = await self.repo.get_all_by_resume_id(resume_id)
        for elem in history:
            elem.created_at = self.__update_timezone(elem, time_zone)
        return history
    
    def __update_timezone(self, history: ResumeImprovementHistory, time_zone: str) -> datetime:
        """Изменяет часовой пояс

        Args:
            history (ResumeImprovementHistory): объект ResumeImprovementHistory
            time_zone (str): Часовой пояс

        Returns:
            datetime: Объект datetime c часовым поясом
        """
        user_tz = ZoneInfo(time_zone)
        history.created_at = history.created_at.replace(tzinfo=timezone.utc)
        return history.created_at.astimezone(user_tz)

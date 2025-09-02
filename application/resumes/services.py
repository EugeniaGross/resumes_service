from typing import Optional, List

from resumes.repositories import ResumesAbstractRepository
from resumes.models import Resume
from resumes.schemes import ResumeBaseScheme, ResumeUpdateScheme


class ResumeService:
    """
    Сервис для работы с резюме и историей улучшений.
    Инкапсулирует бизнес-логику:
    - добавление, получение, обновление и удаление резюме;
    - добавление истории улучшения резюме.

    Внешние зависимости: ResumesAbstractRepository.
    """

    def __init__(self, repo: ResumesAbstractRepository):
        """
        Инициализация сервиса резюме.
        Args:
            repo (ResumesAbstractRepository): Репозиторий для работы с БД.
        """
        self.repo: ResumesAbstractRepository = repo

    async def add_one(self, resume: ResumeBaseScheme, user_id: int) -> Resume:
        """
        Добавляет новое резюме.
        Args:
            resume (ResumeBaseScheme): Данные для создания резюме.
        Returns:
            Resume: Созданное резюме.
        """
        resume = resume.model_dump()
        resume["user_id"] = user_id
        return await self.repo.add_one(resume)

    async def get_one_by_user_id(self, resume_id: int, user_id: int) -> Optional[Resume]:
        """
        Получает одно резюме по его id и id пользователю.
        Args:
            resume_id (int): Идентификатор резюме.
            user_id (int): Идентификатор пользователя.
        Returns:
            Optional[Resume]: Резюме или None.
        """
        return await self.repo.get_one_by_user_id(resume_id, user_id)

    async def get_all_by_user_id(self, user_id: int) -> List[Resume]:
        """
        Получает список всех резюме пользователя.
        Args:
            user_id (int): Идентификатор пользователя.
        Returns:
            List[Resume]: Список резюме.
        """
        return await self.repo.get_all_by_user_id(user_id)

    async def update_one_by_user_id(
        self, resume_id: int, user_id: int, resume: ResumeUpdateScheme
    ) -> Optional[Resume]:
        """
        Обновляет существующее резюме.
        Args:
            resume_id (int): Идентификатор резюме.
            user_id (int): Идентификатор пользователя.
            resume (ResumeUpdateScheme): Данные для обновления.
        Returns:
            Optional[Resume]: Обновлённое резюме или None.
        """
        return await self.repo.update_one_by_user_id(
            resume_id, user_id, resume.model_dump(exclude_unset=True)
        )

    async def delete_one_by_user_id(self, resume_id: int, user_id: int) -> bool:
        """
        Удаляет резюме.
        Args:
            resume_id (int): Идентификатор резюме.
            user_id (int): Идентификатор пользователя.
        Returns:
            bool: True, если удалено, False если резюме не найдено.
        """
        return await self.repo.delete_one_by_user_id(resume_id, user_id)

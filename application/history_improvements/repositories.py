# repositories/resumes.py
from abc import ABC, abstractmethod
from typing import Optional, List
from sqlalchemy import select, desc

from database import async_session
from history_improvements.models import ResumeImprovementHistory
from resumes.models import Resume


class ResumeImprovementHistoryAbstractRepository(ABC):
    """
    Абстрактный репозиторий для работы с историей улучшения резюме.

    Определяет интерфейс для CRUD-операций с историей улучшений резюме:
    - добавление записи;
    """

    @abstractmethod
    async def add_one(
        self, resume_id: int, improved_text: str
    ) -> ResumeImprovementHistory:
        """
        Добавляет запись об улучшении резюме.
        Args:
            resume_id (int): Идентификатор резюме.
            improved_text (str): Текст улучшенного резюме.
        Returns:
            ResumeImprovementHistory: Созданная запись истории.
        """
        raise NotImplementedError
    
    @abstractmethod
    async def get_all_by_resume_id(self, resume_id: int) -> List[ResumeImprovementHistory]:
        """
        Получает всю историю улучшений резюме Пользователя
        Returns:
            list[ResumeImprovementHistory]: Список улучшений резюме.
        """
        raise NotImplementedError


class ResumeImprovementHistoryPostgreSQLRepository(
    ResumeImprovementHistoryAbstractRepository
):
    """
    Реализация репозитория истории улучшения резюме с использованием
    PostgreSQL (SQLModel + AsyncSession).
    """

    @staticmethod
    async def add_one(resume_id: int, improved_content: str) -> ResumeImprovementHistory:
        async with async_session() as session:
            query = select(Resume).where(
                Resume.id == resume_id
            )
            result = await session.execute(query)
            resume = result.scalar_one_or_none()
            if not resume:
                return None
            setattr(resume, "content", improved_content)
            history = ResumeImprovementHistory(
                resume_id=resume.id, improved_content=improved_content
            )
            session.add(history)
            await session.commit()
            await session.refresh(history)
            return history
        
    @staticmethod
    async def get_all_by_resume_id(resume_id: int) -> List[ResumeImprovementHistory]:
        async with async_session() as session:
            query = select(ResumeImprovementHistory).where(
                ResumeImprovementHistory.resume_id == resume_id
            ).order_by(desc(ResumeImprovementHistory.created_at))
            result = await session.execute(query)
            return result.scalars().all()

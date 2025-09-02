# repositories/resumes.py
from abc import ABC, abstractmethod
from typing import Optional, List
from sqlalchemy import select

from database import async_session
from history_improvements.models import ResumeImprovementHistory


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
            history = ResumeImprovementHistory(
                resume_id=resume_id, improved_content=improved_content
            )
            session.add(history)
            await session.commit()
            await session.refresh(history)
            return history

from abc import ABC, abstractmethod
from typing import Optional, List
from sqlalchemy import select

from database import async_session
from resumes.models import Resume


class ResumesAbstractRepository(ABC):
    """
    Абстрактный репозиторий для работы с резюме.

    Определяет интерфейс для CRUD-операций с резюме:
    - создание;
    - получение одного;
    - получение списка;
    - обновление;
    - удаление.
    """

    @abstractmethod
    async def add_one(self, data: dict) -> Resume:
        """
        Создаёт новое резюме.
        Args:
            data (dict): Данные для создания резюме.
        Returns:
            Resume: Резюме.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_one_by_user_id(self, resume_id: int, user_id: int) -> Optional[Resume]:
        """
        Получает резюме по идентификатору резюме и идентификатору пользователя.
        Args:
            resume_id (int): Идентификатор резюме.
            user_id (int): Идентификатор пользователя.
        Returns:
            Optional[Resume]: Резюме или None.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_user_id(self, user_id: int) -> List[Resume]:
        """
        Возвращает список всех резюме пользователя.
        Args:
            user_id (int): Идентификатор пользователя.
        Returns:
            List[Resume]: Список резюме.
        """
        raise NotImplementedError

    @abstractmethod
    async def update_one_by_user_id(
        self, resume_id: int, user_id: int, data: dict
    ) -> Optional[Resume]:
        """
        Обновляет существующее резюме.
        Args:
            resume_id (int): Идентификатор резюме.
            user_id (int): Идентификатор пользователя.
            data (dict): Данные для обновления.
        Returns:
            Optional[Resume]: Обновлённое резюме или None.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_one_by_user_id(self, resume_id: int, user_id: int) -> bool:
        """
        Удаляет резюме.
        Args:
            resume_id (int): Идентификатор резюме.
            user_id (int): Идентификатор пользователя.
        Returns:
            bool: True, если удаление успешно, False если резюме не найдено.
        """
        raise NotImplementedError


class ResumesPostgreSQLRepository(ResumesAbstractRepository):
    """
    Реализация репозитория резюме с использованием PostgreSQL (SQLModel + AsyncSession).
    """

    @staticmethod
    async def add_one(data: dict) -> Resume:
        async with async_session() as session:
            resume = Resume(**data)
            session.add(resume)
            await session.commit()
            await session.refresh(resume)
            return resume

    @staticmethod
    async def get_one_by_user_id(resume_id: int, user_id: int) -> Optional[Resume]:
        async with async_session() as session:
            query = select(Resume).where(
                Resume.id == resume_id, Resume.user_id == user_id
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @staticmethod
    async def get_all_by_user_id(user_id: int) -> List[Resume]:
        async with async_session() as session:
            query = select(Resume).where(Resume.user_id == user_id)
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def update_one_by_user_id(
        resume_id: int, user_id: int, data: dict
    ) -> Optional[Resume]:
        async with async_session() as session:
            query = select(Resume).where(
                Resume.id == resume_id, Resume.user_id == user_id
            )
            result = await session.execute(query)
            resume = result.scalar_one_or_none()
            if not resume:
                return None
            for key, value in data.items():
                setattr(resume, key, value)
            await session.commit()
            await session.refresh(resume)
            return resume

    @staticmethod
    async def delete_one_by_user_id(resume_id: int, user_id: int) -> bool:
        async with async_session() as session:
            query = select(Resume).where(
                Resume.id == resume_id, Resume.user_id == user_id
            )
            result = await session.execute(query)
            resume = result.scalar_one_or_none()
            if not resume:
                return False
            await session.delete(resume)
            await session.commit()
            return True

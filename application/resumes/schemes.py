from typing import Optional

from sqlmodel import SQLModel


class ResumeBaseScheme(SQLModel):
    """Базовая схема для резюме."""

    title: str
    content: str


class ResumeUpdateScheme(SQLModel):
    """Схема для обновления резюме."""

    title: Optional[str] = None
    content: Optional[str] = None


class ResumeResponseScheme(ResumeBaseScheme):
    """Схема для отдачи резюме наружу."""

    id: int
    user_id: int

    class Config:
        orm_mode = True

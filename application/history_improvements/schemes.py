from datetime import datetime

from sqlmodel import SQLModel


class ResumeImprovementResponseScheme(SQLModel):
    """Схема для отображения истории улучшений резюме."""

    id: int
    resume_id: int
    improved_content: str
    created_at: datetime

    class Config:
        from_attributes = True

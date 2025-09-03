from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, text

if TYPE_CHECKING:
    from resumes.models import Resume


class ResumeImprovementHistory(SQLModel, table=True):
    """
    ORM-модель истории улучшений резюме для хранения в базе данных.
    Attrs:
        id (int): Уникальный идентификатор улучшения резюме (Primary Key).
        resume_id (int): Идентификатор резюме.
        improved_content (str): Улучшение.
        created_at (datetime): Дата и время создания улучшения резюме
        resume (Resume): Экземпляр резюме
    """

    __tablename__ = "resume_improvement_history"
    __table_args__ = {"extend_existing": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    resume_id: int = Field(
        foreign_key="resumes.id"
    )
    improved_content: str
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": text("TIMEZONE('utc', now())")}
    )

    resume: "Resume" = Relationship(back_populates="improvements")

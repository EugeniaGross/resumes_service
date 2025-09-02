from datetime import datetime
from typing import TYPE_CHECKING

from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, text

if TYPE_CHECKING:
    from history_improvements.models import ResumeImprovementHistory


class Resume(SQLModel, table=True):
    """
    ORM-модель резюме для хранения в базе данных.
    Атрибуты:
        id (int): Уникальный идентификатор резюме (Primary Key).
        user_id (int): Идентификатор пользователя.
        improved_content (str): Улучшение.
        title (str): Заголовок резюме
        content (str): Содержание резюме
        improvements (List[ResumeImprovement]): История улучшений резюме
    """

    __tablename__ = "resumes"
    __table_args__ = {"extend_existing": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    title: str
    content: str
    created_at: datetime = Field(
        sa_column_kwargs={"server_default": text("TIMEZONE('utc', now())")}
    )

    improvements: List["ResumeImprovementHistory"] = Relationship(
        back_populates="resume"
    )

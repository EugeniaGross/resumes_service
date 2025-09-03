from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request

from base_dependiences import get_current_user
from history_improvements.dependiences import history_improvement_resume_service
from history_improvements.services import ResumeImprovementHistoryService
from history_improvements.schemes import ResumeImprovementResponseScheme
from resumes.dependiences import resumes_service
from resumes.services import ResumeService
from utils.improve_service import ImproveClient

router = APIRouter(
    prefix="/api/v1/resumes", 
    tags=["Resume"],
    dependencies=[Depends(get_current_user)]
)


@router.post("/{resume_id}/improve", response_model=ResumeImprovementResponseScheme)
async def improve_resume(
    resume_id: int,
    request: Request,
    resume_service: ResumeService = Depends(resumes_service),
    history_improvement_service: ResumeImprovementHistoryService = Depends(
        history_improvement_resume_service
    ),
    improve_client: ImproveClient = Depends(ImproveClient),
    time_zone: str = "UTC"
):
    """
    Улучшение текста резюме (заглушка).

    Функция выполняет следующие шаги:
    1. Получает резюме по идентификатору и пользователю.
    2. Проверяет, существует ли резюме.
    3. Добавляет к тексту резюме строку " [Improved]" как заглушку улучшения.
    4. Сохраняет результат в историю улучшений резюме.
    5. Возвращает объект с информацией об улучшенном резюме.

    Args:
        resume_id (int): Идентификатор резюме, которое нужно улучшить.
        request (Request): Объект FastAPI Request, используется для извлечения
            user_id.
        resume_service (ResumeService): Сервис для работы с резюме.
        history_improvement_resume_service (ResumeImprovementHistoryService):
            Сервис для сохранения истории улучшений.
        improve_client (ImproveClient): Клиент для улучшения содержания текста
        time_zone (str): Часовой пояс
    Returns:
        ResumeImprovementResponseScheme: Объект с улучшенным текстом резюме и
            информацией о сохранении в историю.

    Raises:
        HTTPException: Если резюме с указанным resume_id и user_id не найдено
            (код 404).
    """
    user_id = request.state.user_id
    resume = await resume_service.get_one_by_user_id(resume_id, user_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Резюме не найдено")
    improved_content = improve_client.improve_resume(resume.content)
    return await history_improvement_service.add_one(
        resume.id, 
        improved_content,
        time_zone
    )

@router.get("/{resume_id}/history_improvements", response_model=List[ResumeImprovementResponseScheme])
async def get_history_improvements_resume(
    resume_id: int,
    request: Request,
    resume_service: ResumeService = Depends(resumes_service),
    history_improvement_service: ResumeImprovementHistoryService = Depends(
        history_improvement_resume_service
    ),
    time_zone: str = "UTC"
):
    """
    История улучшений резюме.

    Функция выполняет следующие шаги:
    1. Получает резюме по идентификатору и пользователю.
    2. Проверяет, существует ли резюме.
    3. Получает список улучшений резюме.
    5. Возвращает список улучшений резюме.

    Args:
        resume_id (int): Идентификатор резюме, которое нужно улучшить.
        request (Request): Объект FastAPI Request, используется для извлечения
            user_id.
        resume_service (ResumeService): Сервис для работы с резюме.
        history_improvement_resume_service (ResumeImprovementHistoryService):
            Сервис для сохранения истории улучшений.
        time_zone (str): Часовой пояс
    Returns:
        List[ResumeImprovementResponseScheme]: Список объектов с улучшенным текстом резюме и
            информацией о сохранении в историю.

    Raises:
        HTTPException: Если резюме с указанным resume_id и user_id не найдено
            (код 404).
    """
    user_id = request.state.user_id
    resume = await resume_service.get_one_by_user_id(resume_id, user_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Резюме не найдено")
    return await history_improvement_service.get_all_by_resume_id(
        resume.id,
        time_zone
    )

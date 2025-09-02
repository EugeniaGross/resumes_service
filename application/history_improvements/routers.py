from fastapi import APIRouter, Depends, HTTPException, Request

from history_improvements.dependiences import history_improvement_resume_service
from history_improvements.services import ResumeImprovementHistoryService
from history_improvements.schemes import ResumeImprovementResponseScheme
from resumes.dependiences import resumes_service
from resumes.services import ResumeService

router = APIRouter(prefix="/api/v1/resumes", tags=["Resume"])


@router.post("/{resume_id}/improve", response_model=ResumeImprovementResponseScheme)
async def improve_resume(
    resume_id: int,
    request: Request,
    resume_service: ResumeService = Depends(resumes_service),
    history_improvement_service: ResumeImprovementHistoryService = Depends(
        history_improvement_resume_service
    ),
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
        user_id (int): Идентификатор пользователя (может быть перезаписан из
            request.state.user_id).
        request (Request): Объект FastAPI Request, используется для извлечения
            user_id.
        resume_service (ResumeService): Сервис для работы с резюме.
        history_improvement_resume_service (ResumeImprovementHistoryService):
            Сервис для сохранения истории улучшений.

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
    improved_content = resume.content + " [Improved]"
    return await history_improvement_service.add_one(resume.id, improved_content)

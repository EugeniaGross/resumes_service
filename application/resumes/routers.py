from fastapi import APIRouter, Depends, HTTPException, Request, status

from resumes.dependiences import resumes_service
from resumes.services import ResumeService
from resumes.schemes import ResumeBaseScheme, ResumeResponseScheme, ResumeUpdateScheme

router = APIRouter(prefix="/api/v1/resumes", tags=["Resume"])


@router.post(
    "/", response_model=ResumeResponseScheme, status_code=status.HTTP_201_CREATED
)
async def create_resume(
    request: Request,
    resume: ResumeBaseScheme,
    resume_service: ResumeService = Depends(resumes_service),
):
    """
    Создать новое резюме для пользователя.
    Args:
        request (Request): Объект FastAPI Request, используется для извлечения user_id.
        resume (ResumeBaseScheme): Данные резюме для создания.
        resume_service (ResumeService): Сервис для работы с резюме.
    Returns:
        ResumeResponseScheme: Резюме пользователя.
    """
    user_id = request.state.user_id
    return await resume_service.add_one(resume, user_id)


@router.get("/", response_model=list[ResumeResponseScheme])
async def list_resumes(
    request: Request, resume_service: ResumeService = Depends(resumes_service)
):
    """
    Получить список всех резюме пользователя.
    Args:
        request (Request): Объект FastAPI Request для извлечения user_id.
        resume_service (ResumeService): Сервис для работы с резюме.
    Returns:
        list[ResumeResponseScheme]: Список резюме пользователя.
    """
    user_id = request.state.user_id
    return await resume_service.get_all_by_user_id(user_id)


@router.get("/{resume_id}", response_model=ResumeResponseScheme)
async def get_resume(
    resume_id: int,
    request: Request,
    resume_service: ResumeService = Depends(resumes_service),
):
    """
    Получить конкретное резюме по его идентификатору.
    Args:
        resume_id (int): Идентификатор резюме.
        request (Request): Объект FastAPI Request для извлечения user_id.
        resume_service (ResumeService): Сервис для работы с резюме.
    Returns:
        ResumeResponseScheme: Данные запрошенного резюме.
    Raises:
        HTTPException: Если резюме с указанным ID не найдено (код 404).
    """
    user_id = request.state.user_id
    resume = await resume_service.get_one_by_user_id(resume_id, user_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Резюме не найдено")
    return resume


@router.patch("/{resume_id}", response_model=ResumeResponseScheme)
async def update_resume(
    resume_id: int,
    request: Request,
    resume: ResumeUpdateScheme,
    resume_service: ResumeService = Depends(resumes_service),
):
    """
    Обновить данные существующего резюме.
    Args:
        resume_id (int): Идентификатор резюме.
        request (Request): Объект FastAPI Request для извлечения user_id.
        resume (ResumeUpdateScheme): Данные для обновления резюме.
        resume_service (ResumeService): Сервис для работы с резюме.
    Returns:
        ResumeResponseScheme: Резюме пользователя.
    Raises:
        HTTPException: Если резюме с указанным ID не найдено (код 404).
    """
    user_id = request.state.user_id
    updated = await resume_service.update_one_by_user_id(resume_id, user_id, resume)
    if not updated:
        raise HTTPException(status_code=404, detail="Резюме не найдено")
    return updated


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: int,
    request: Request,
    resume_service: ResumeService = Depends(resumes_service),
):
    """
    Удалить резюме пользователя.

    Args:
        resume_id (int): Идентификатор резюме для удаления.
        request (Request): Объект FastAPI Request для извлечения user_id.
        resume_service (ResumeService): Сервис для работы с резюме.
    Returns:
        None
    Raises:
        HTTPException: Если резюме с указанным ID не найдено (код 404).
    """
    user_id = request.state.user_id
    deleted = await resume_service.delete_one_by_user_id(resume_id, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Резюме не найдено")
    return

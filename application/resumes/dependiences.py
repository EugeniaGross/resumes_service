from resumes.repositories import ResumesPostgreSQLRepository
from resumes.services import ResumeService


def resumes_service():
    return ResumeService(ResumesPostgreSQLRepository)

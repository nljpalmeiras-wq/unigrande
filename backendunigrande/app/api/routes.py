from fastapi import APIRouter

from app.api import alunos, cursos, disciplinas, professores

api_router = APIRouter()

api_router.include_router(cursos.router, prefix="/cursos", tags=["cursos"])

api_router.include_router(
    professores.router, prefix="/professores", tags=["professores"]
)

api_router.include_router(alunos.router, prefix="/alunos", tags=["alunos"])

api_router.include_router(
    disciplinas.router, prefix="/disciplinas", tags=["disciplinas"]
)

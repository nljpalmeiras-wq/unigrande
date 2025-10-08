from fastapi import APIRouter

from app.api import cursos

api_router = APIRouter()

api_router.include_router(cursos.router, prefix="/cursos", tags=["cursos"])

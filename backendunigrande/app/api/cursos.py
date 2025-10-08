from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException, Response, status
from tortoise.exceptions import (DoesNotExist, IntegrityError,
                                 MultipleObjectsReturned)
from tortoise.transactions import in_transaction

from app.auth.utils import setup_logger
from app.schemas.unigrande import CursoCreate, CursoResponse, CursoUpdate
from app.services.unigrande import CursoService

# Configurar o logger
logger = setup_logger()

router = APIRouter()


# =============== util de erro ===============
async def error_500(e: Exception):
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Ocorreu um erro inesperado: {str(e)}",
    )


# ----------------------------------------------------------------------
# Curso
# ----------------------------------------------------------------------
@router.post("/create-curso", response_model=CursoResponse, status_code=201)
async def create_curso(payload: CursoCreate):
    async with in_transaction():
        try:
            obj = await CursoService.create(payload)
            return await CursoService.response(obj)
        except IntegrityError as e:
            raise HTTPException(409, f"Restrição de integridade: {e}")
        except Exception as e:
            await error_500(e)


@router.get("/buscar-curso/{id}", response_model=CursoResponse)
async def get_curso(id: int):
    try:
        obj = await CursoService.get(id)
        return await CursoService.response(obj)
    except (DoesNotExist, MultipleObjectsReturned):
        raise HTTPException(404, "Curso não encontrado")
    except Exception as e:
        await error_500(e)


@router.get("/listar-cursos", response_model=List[CursoResponse])
async def list_cursos():
    try:
        rows = await CursoService.list_all()
        return [await CursoService.response(x) for x in rows]
    except Exception as e:
        await error_500(e)


@router.put("/atualizar-curso/{id}", response_model=CursoResponse)
async def update_curso(id: int, payload: CursoUpdate):
    async with in_transaction():
        try:
            obj = await CursoService.update(id, payload)
            return await CursoService.response(obj)
        except HTTPException as e:
            raise e
        except Exception as e:
            await error_500(e)


@router.delete("/delete-curso/{id}", status_code=204)
async def delete_curso(id: int):
    async with in_transaction():
        try:
            await CursoService.delete(id)
            return Response(status_code=204)
        except HTTPException as e:
            raise e
        except Exception as e:
            await error_500(e)

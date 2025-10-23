# app/api/disciplinas.py
from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException, Response, status
from tortoise.exceptions import (DoesNotExist, IntegrityError,
                                 MultipleObjectsReturned)
from tortoise.transactions import in_transaction

from app.auth.utils import setup_logger
from app.schemas.unigrande import (DisciplinaCreate, DisciplinaResponse,
                                   DisciplinaUpdate)
from app.services.unigrande import DisciplinaService

logger = setup_logger()
router = APIRouter()


# =============== util de erro ===============
async def error_500(e: Exception):
    # se já for HTTPException (ex.: 404/409), apenas repasse
    if isinstance(e, HTTPException):
        raise e
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Ocorreu um erro inesperado: {str(e)}",
    )


# ----------------------------------------------------------------------
# Disciplina
# ----------------------------------------------------------------------
@router.post("/create-disciplina", response_model=DisciplinaResponse, status_code=201)
async def create_disciplina(payload: DisciplinaCreate):
    """
    Cria uma disciplina.
    Campos esperados (schema): nome, creditos, tipo, horas_obrig, limite_faltas.
    """
    async with in_transaction():
        try:
            obj = await DisciplinaService.create(payload)
            return await DisciplinaService.response(obj)
        except IntegrityError as e:
            raise HTTPException(
                status_code=409, detail=f"Restrição de integridade: {e}"
            )
        except Exception as e:
            await error_500(e)


@router.get("/buscar-disciplina/{id}", response_model=DisciplinaResponse)
async def get_disciplina(id: int):
    """
    Busca uma disciplina pelo ID (PK).
    """
    try:
        obj = await DisciplinaService.get(id)
        return await DisciplinaService.response(obj)
    except (DoesNotExist, MultipleObjectsReturned):
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    except HTTPException as e:
        raise e
    except Exception as e:
        await error_500(e)


@router.get("/listar-disciplinas", response_model=List[DisciplinaResponse])
async def list_disciplinas():
    """
    Lista todas as disciplinas.
    """
    try:
        rows = await DisciplinaService.list_all()
        return [await DisciplinaService.response(x) for x in rows]
    except Exception as e:
        await error_500(e)


@router.put("/atualizar-disciplina/{id}", response_model=DisciplinaResponse)
async def update_disciplina(id: int, payload: DisciplinaUpdate):
    """
    Atualiza dados da disciplina (somente campos enviados).
    """
    async with in_transaction():
        try:
            obj = await DisciplinaService.update(id, payload)
            return await DisciplinaService.response(obj)
        except HTTPException as e:
            raise e
        except Exception as e:
            await error_500(e)


@router.delete("/delete-disciplina/{id}", status_code=204)
async def delete_disciplina(id: int):
    """
    Exclui uma disciplina.
    """
    async with in_transaction():
        try:
            await DisciplinaService.delete(id)
            return Response(status_code=204)
        except HTTPException as e:
            raise e
        except Exception as e:
            await error_500(e)

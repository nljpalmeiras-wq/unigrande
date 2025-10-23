# app/api/alunos.py
from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException, Response, status
from tortoise.exceptions import (DoesNotExist, IntegrityError,
                                 MultipleObjectsReturned)
from tortoise.transactions import in_transaction

from app.auth.utils import setup_logger
from app.schemas.unigrande import AlunoCreate, AlunoResponse, AlunoUpdate
from app.services.unigrande import AlunoService

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
# Aluno
# ----------------------------------------------------------------------
@router.post("/create-aluno", response_model=AlunoResponse, status_code=201)
async def create_aluno(payload: AlunoCreate):
    """
    Cria um aluno. A FK `curso_id` deve existir.
    """
    async with in_transaction():
        try:
            obj = await AlunoService.create(payload)
            return await AlunoService.response(obj)
        except IntegrityError as e:
            # violações de FK/unique/etc.
            raise HTTPException(
                status_code=409, detail=f"Restrição de integridade: {e}"
            )
        except Exception as e:
            await error_500(e)


@router.get("/buscar-aluno/{matricula}", response_model=AlunoResponse)
async def get_aluno(matricula: int):
    """
    Busca um aluno pela matrícula (PK).
    """
    try:
        obj = await AlunoService.get(matricula)
        return await AlunoService.response(obj)
    except (DoesNotExist, MultipleObjectsReturned):
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    except HTTPException as e:
        raise e
    except Exception as e:
        await error_500(e)


@router.get("/listar-alunos", response_model=List[AlunoResponse])
async def list_alunos():
    """
    Lista todos os alunos.
    """
    try:
        rows = await AlunoService.list_all()
        return [await AlunoService.response(x) for x in rows]
    except Exception as e:
        await error_500(e)


@router.put("/atualizar-aluno/{matricula}", response_model=AlunoResponse)
async def update_aluno(matricula: int, payload: AlunoUpdate):
    """
    Atualiza dados do aluno. Se `curso_id` vier no payload, valida a existência do curso no service.
    """
    async with in_transaction():
        try:
            obj = await AlunoService.update(matricula, payload)
            return await AlunoService.response(obj)
        except HTTPException as e:
            # por exemplo, 404 do service ou 409 custom
            raise e
        except Exception as e:
            await error_500(e)


@router.delete("/delete-aluno/{matricula}", status_code=204)
async def delete_aluno(matricula: int):
    """
    Exclui um aluno.
    """
    async with in_transaction():
        try:
            await AlunoService.delete(matricula)
            return Response(status_code=204)
        except HTTPException as e:
            raise e
        except Exception as e:
            await error_500(e)

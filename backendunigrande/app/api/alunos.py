# app/api/alunos.py
from __future__ import annotations

from pathlib import Path
from typing import List

from fastapi import APIRouter, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from tortoise.exceptions import (DoesNotExist, IntegrityError,
                                 MultipleObjectsReturned)
from tortoise.transactions import in_transaction

from app.auth.utils import setup_logger
from app.schemas.unigrande import (AlunoCreate, AlunoListPaginated,
                                   AlunoResponse, AlunoUpdate)
from app.services.unigrande import AlunoService

logger = setup_logger()
router = APIRouter()

# BASE_DIR = app/
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


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


@router.get("/listar-alunos-paginado", response_model=AlunoListPaginated)
async def list_alunos_paginado(limit: int = 10, offset: int = 0):
    """
    Lista alunos com paginação (limit/offset).
    Exemplo:
      /alunos/listar-alunos-paginado?limit=20&offset=0
    """
    try:
        rows, total = await AlunoService.list_paginated(limit=limit, offset=offset)
        return AlunoListPaginated(
            total=total,
            limit=limit,
            offset=offset,
            results=[await AlunoService.response(x) for x in rows],
        )
    except Exception as e:
        await error_500(e)


@router.get("/list-alunos/view", response_class=HTMLResponse)
async def alunos_view(
    request: Request,
    limit: int = 10,
    offset: int = 0,
):
    """
    Tela HTML com listagem paginada de alunos.
    Exemplo:
      /alunos/view?limit=20&offset=0
    """
    try:
        rows, total = await AlunoService.list_paginated(limit=limit, offset=offset)
        alunos = [await AlunoService.response(x) for x in rows]

        # cálculo básico de paginação
        page = (offset // limit) + 1 if limit > 0 else 1
        total_pages = (total + limit - 1) // limit if limit > 0 else 1

        next_offset = offset + limit if page < total_pages else None
        prev_offset = offset - limit if offset - limit >= 0 else None

        return templates.TemplateResponse(
            "alunos.html",
            {
                "request": request,
                "titulo_pagina": "Lista de Alunos",
                "alunos": alunos,
                "total": total,
                "limit": limit,
                "offset": offset,
                "page": page,
                "total_pages": total_pages,
                "next_offset": next_offset,
                "prev_offset": prev_offset,
            },
        )
    except Exception as e:
        await error_500(e)

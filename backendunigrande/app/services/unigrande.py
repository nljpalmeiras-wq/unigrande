# app/services/unigrande.py
from __future__ import annotations

from fastapi import HTTPException, status

from app.models.unigrande import (Aluno, Curso, Disciplina, Historico,
                                  Matricula, Matriz, PeriodoLetivo, Professor,
                                  Turma)
from app.schemas.unigrande import (AlunoCreate, AlunoResponse, AlunoSummary,
                                   AlunoUpdate, CursoCreate, CursoResponse,
                                   CursoSummary, CursoUpdate, DisciplinaCreate,
                                   DisciplinaResponse, DisciplinaSummary,
                                   DisciplinaUpdate, HistoricoCreate,
                                   HistoricoResponse, HistoricoUpdate,
                                   MatriculaCreate, MatriculaResponse,
                                   MatriculaUpdate, MatrizCreate,
                                   MatrizResponse, MatrizUpdate,
                                   PeriodoLetivoCreate, PeriodoLetivoResponse,
                                   PeriodoLetivoSummary, PeriodoLetivoUpdate,
                                   ProfessorCreate, ProfessorResponse,
                                   ProfessorSummary, ProfessorUpdate,
                                   TurmaCreate, TurmaResponse, TurmaSummary,
                                   TurmaUpdate)


# =========================
# Funções utilitárias comuns
# =========================
async def _ensure_exists(model, **filters):
    obj = await model.get_or_none(**filters)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.__name__} não encontrado.",
        )
    return obj


# =========================
# PeriodoLetivo
# =========================
class PeriodoLetivoService:
    @staticmethod
    async def create(payload: PeriodoLetivoCreate) -> PeriodoLetivo:
        # unique (ano, semestre)
        exists = await PeriodoLetivo.get_or_none(
            ano=payload.ano, semestre=payload.semestre
        )
        if exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Período letivo já existe para (ano, semestre).",
            )
        obj = PeriodoLetivo(**payload.model_dump())
        await obj.save()
        return obj

    @staticmethod
    async def update(id_: int, payload: PeriodoLetivoUpdate) -> PeriodoLetivo:
        obj = await _ensure_exists(PeriodoLetivo, id=id_)
        data = payload.model_dump(exclude_unset=True)
        # se alterar ano/semestre, garanta unicidade
        if {"ano", "semestre"} & data.keys():
            ano = data.get("ano", obj.ano)
            semestre = data.get("semestre", obj.semestre)
            other = await PeriodoLetivo.get_or_none(ano=ano, semestre=semestre)
            if other and other.id != obj.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Outro período letivo já usa este (ano, semestre).",
                )
        for k, v in data.items():
            setattr(obj, k, v)
        await obj.save()
        return obj

    @staticmethod
    async def delete(id_: int) -> None:
        obj = await _ensure_exists(PeriodoLetivo, id=id_)
        await obj.delete()

    @staticmethod
    async def get(id_: int) -> PeriodoLetivo:
        return await _ensure_exists(PeriodoLetivo, id=id_)

    @staticmethod
    async def list_all():
        return await PeriodoLetivo.all()

    @staticmethod
    async def response(obj: PeriodoLetivo) -> PeriodoLetivoResponse:
        return PeriodoLetivoResponse(
            id=obj.id,
            ano=obj.ano,
            semestre=obj.semestre,
            data_inicio=obj.data_inicio,
            data_fim=obj.data_fim,
        )


# =========================
# Professor
# =========================
class ProfessorService:
    @staticmethod
    async def create(payload: ProfessorCreate) -> Professor:
        exists = await Professor.get_or_none(id=payload.id)
        if exists:
            raise HTTPException(
                status_code=409, detail="Professor com este ID já existe."
            )
        obj = Professor(**payload.model_dump())
        await obj.save()
        return obj

    @staticmethod
    async def update(id_: int, payload: ProfessorUpdate) -> Professor:
        obj = await _ensure_exists(Professor, id=id_)
        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(obj, k, v)
        await obj.save()
        return obj

    @staticmethod
    async def delete(id_: int) -> None:
        obj = await _ensure_exists(Professor, id=id_)
        await obj.delete()

    @staticmethod
    async def get(id_: int) -> Professor:
        return await _ensure_exists(Professor, id=id_)

    @staticmethod
    async def list_all():
        return await Professor.all()

    @staticmethod
    async def response(obj: Professor) -> ProfessorResponse:
        return ProfessorResponse(id=obj.id, matricula=obj.matricula, nome=obj.nome)


# =========================
# Curso
# =========================
class CursoService:
    @staticmethod
    async def create(payload: CursoCreate) -> Curso:
        if payload.coordenador_id:
            await _ensure_exists(Professor, id=payload.coordenador_id)
        exists = await Curso.get_or_none(id=payload.id)
        if exists:
            raise HTTPException(status_code=409, detail="Curso com este ID já existe.")
        obj = Curso(
            id=payload.id,
            nome=payload.nome,
            total_creditos=payload.total_creditos,
            coordenador_id=payload.coordenador_id or None,
        )
        await obj.save()
        return obj

    @staticmethod
    async def update(id_: int, payload: CursoUpdate) -> Curso:
        obj = await _ensure_exists(Curso, id=id_)
        data = payload.model_dump(exclude_unset=True)

        # Se coordenador_id veio não-nulo, valide existência
        if "coordenador_id" in data and data["coordenador_id"] is not None:
            await _ensure_exists(Professor, id=data["coordenador_id"])

        # Se explicitamente vier null, limpe a FK (deixe sem coordenador)
        if "coordenador_id" in data and data["coordenador_id"] is None:
            obj.coordenador_id = None
            del data["coordenador_id"]

        for k, v in data.items():
            setattr(obj, k, v)

        await obj.save()
        return obj

    @staticmethod
    async def delete(id_: int) -> None:
        obj = await _ensure_exists(Curso, id=id_)
        await obj.delete()

    @staticmethod
    async def get(id_: int):
        obj = await Curso.get_or_none(id=id_).prefetch_related("coordenador")
        if not obj:
            raise HTTPException(status_code=404, detail="Curso não encontrado.")
        return obj

    @staticmethod
    async def list_all():
        return await Curso.all().prefetch_related("coordenador")

    @staticmethod
    async def response(obj: Curso) -> CursoResponse:
        coord = (
            ProfessorSummary(id=obj.coordenador.id, nome=obj.coordenador.nome)
            if getattr(obj, "coordenador", None)
            else None
        )
        return CursoResponse(
            id=obj.id,
            nome=obj.nome,
            total_creditos=obj.total_creditos,
            coordenador_id=obj.coordenador_id,
            coordenador=coord,
        )


# =========================
# Disciplina
# =========================
class DisciplinaService:
    @staticmethod
    async def create(payload: DisciplinaCreate) -> Disciplina:
        exists = await Disciplina.get_or_none(id=payload.id)
        if exists:
            raise HTTPException(
                status_code=409, detail="Disciplina com este ID já existe."
            )
        obj = Disciplina(**payload.model_dump())
        await obj.save()
        return obj

    @staticmethod
    async def update(id_: int, payload: DisciplinaUpdate) -> Disciplina:
        obj = await _ensure_exists(Disciplina, id=id_)
        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(obj, k, v)
        await obj.save()
        return obj

    @staticmethod
    async def delete(id_: int) -> None:
        obj = await _ensure_exists(Disciplina, id=id_)
        await obj.delete()

    @staticmethod
    async def get(id_: int) -> Disciplina:
        return await _ensure_exists(Disciplina, id=id_)

    @staticmethod
    async def list_all():
        return await Disciplina.all()

    @staticmethod
    async def response(obj: Disciplina) -> DisciplinaResponse:
        return DisciplinaResponse(
            id=obj.id,
            nome=obj.nome,
            creditos=obj.creditos,
            tipo=obj.tipo,
            horas_obrig=obj.horas_obrig,
            limite_faltas=obj.limite_faltas,
        )


# =========================
# Matriz (currículo)
# =========================
class MatrizService:
    @staticmethod
    async def create(payload: MatrizCreate) -> Matriz:
        await _ensure_exists(Curso, id=payload.curso_id)
        await _ensure_exists(Disciplina, id=payload.disciplina_id)
        exists = await Matriz.get_or_none(
            curso_id=payload.curso_id, disciplina_id=payload.disciplina_id
        )
        if exists:
            raise HTTPException(
                status_code=409, detail="Matriz já existe para (curso, disciplina)."
            )
        obj = Matriz(**payload.model_dump())
        await obj.save()
        return obj

    @staticmethod
    async def update(id_: int, payload: MatrizUpdate) -> Matriz:
        obj = await _ensure_exists(Matriz, id=id_)
        data = payload.model_dump(exclude_unset=True)
        if "curso_id" in data:
            await _ensure_exists(Curso, id=data["curso_id"])
        if "disciplina_id" in data:
            await _ensure_exists(Disciplina, id=data["disciplina_id"])
        # checa unique se curso/disciplina mudarem
        cur = data.get("curso_id", obj.curso_id)
        dis = data.get("disciplina_id", obj.disciplina_id)
        other = await Matriz.get_or_none(curso_id=cur, disciplina_id=dis)
        if other and other.id != obj.id:
            raise HTTPException(
                status_code=409, detail="Outra Matriz já usa (curso, disciplina)."
            )
        for k, v in data.items():
            setattr(obj, k, v)
        await obj.save()
        return obj

    @staticmethod
    async def delete(id_: int) -> None:
        obj = await _ensure_exists(Matriz, id=id_)
        await obj.delete()

    @staticmethod
    async def get(id_: int) -> Matriz:
        return await _ensure_exists(Matriz, id=id_)

    @staticmethod
    async def list_all():
        return await Matriz.all().prefetch_related("curso", "disciplina")

    @staticmethod
    async def response(obj: Matriz) -> MatrizResponse:
        return MatrizResponse(
            id=obj.id,
            curso_id=obj.curso_id,
            disciplina_id=obj.disciplina_id,
            periodo=obj.periodo,
            curso=CursoSummary(id=obj.curso.id, nome=obj.curso.nome),
            disciplina=DisciplinaSummary(
                id=obj.disciplina.id,
                nome=obj.disciplina.nome,
                creditos=obj.disciplina.creditos,
            ),
        )


# =========================
# Turma (oferta)
# =========================
class TurmaService:
    @staticmethod
    async def create(payload: TurmaCreate) -> Turma:
        await _ensure_exists(PeriodoLetivo, id=payload.periodo_letivo_id)
        await _ensure_exists(Curso, id=payload.curso_id)
        await _ensure_exists(Disciplina, id=payload.disciplina_id)
        if payload.professor_id:
            await _ensure_exists(Professor, id=payload.professor_id)
        # unique (periodo_letivo, curso, disciplina)
        exists = await Turma.get_or_none(
            periodo_letivo_id=payload.periodo_letivo_id,
            curso_id=payload.curso_id,
            disciplina_id=payload.disciplina_id,
        )
        if exists:
            raise HTTPException(
                status_code=409,
                detail="Turma já ofertada neste período/curso/disciplina.",
            )
        obj = Turma(**payload.model_dump())
        await obj.save()
        return obj

    @staticmethod
    async def update(id_: int, payload: TurmaUpdate) -> Turma:
        obj = await _ensure_exists(Turma, id=id_)
        data = payload.model_dump(exclude_unset=True)
        # valida FKs se vierem
        if "periodo_letivo_id" in data:
            await _ensure_exists(PeriodoLetivo, id=data["periodo_letivo_id"])
        if "curso_id" in data:
            await _ensure_exists(Curso, id=data["curso_id"])
        if "disciplina_id" in data:
            await _ensure_exists(Disciplina, id=data["disciplina_id"])
        if "professor_id" in data and data["professor_id"] is not None:
            await _ensure_exists(Professor, id=data["professor_id"])

        # checa unique
        pl = data.get("periodo_letivo_id", obj.periodo_letivo_id)
        cu = data.get("curso_id", obj.curso_id)
        di = data.get("disciplina_id", obj.disciplina_id)
        other = await Turma.get_or_none(
            periodo_letivo_id=pl, curso_id=cu, disciplina_id=di
        )
        if other and other.id != obj.id:
            raise HTTPException(
                status_code=409, detail="Já existe outra Turma com estes dados."
            )
        for k, v in data.items():
            setattr(obj, k, v)
        await obj.save()
        return obj

    @staticmethod
    async def delete(id_: int) -> None:
        obj = await _ensure_exists(Turma, id=id_)
        await obj.delete()

    @staticmethod
    async def get(id_: int) -> Turma:
        return await _ensure_exists(Turma, id=id_)

    @staticmethod
    async def list_all():
        return await Turma.all().prefetch_related(
            "periodo_letivo", "curso", "disciplina", "professor"
        )

    @staticmethod
    async def response(obj: Turma) -> TurmaResponse:
        return TurmaResponse(
            id=obj.id,
            periodo_letivo_id=obj.periodo_letivo_id,
            curso_id=obj.curso_id,
            disciplina_id=obj.disciplina_id,
            professor_id=obj.professor_id,
            vagas=obj.vagas,
            periodo_letivo=PeriodoLetivoSummary(
                id=obj.periodo_letivo.id,
                ano=obj.periodo_letivo.ano,
                semestre=obj.periodo_letivo.semestre,
            ),
            curso=CursoSummary(id=obj.curso.id, nome=obj.curso.nome),
            disciplina=DisciplinaSummary(
                id=obj.disciplina.id,
                nome=obj.disciplina.nome,
                creditos=obj.disciplina.creditos,
            ),
            professor=(
                ProfessorSummary(id=obj.professor.id, nome=obj.professor.nome)
                if getattr(obj, "professor", None)
                else None
            ),
        )


# =========================
# Aluno
# =========================
class AlunoService:
    @staticmethod
    async def create(payload: AlunoCreate) -> Aluno:
        await _ensure_exists(Curso, id=payload.curso_id)
        exists = await Aluno.get_or_none(matricula=payload.matricula)
        if exists:
            raise HTTPException(
                status_code=409, detail="Aluno com esta matrícula já existe."
            )
        obj = Aluno(**payload.model_dump())
        await obj.save()
        return obj

    @staticmethod
    async def update(matricula: int, payload: AlunoUpdate) -> Aluno:
        obj = await _ensure_exists(Aluno, matricula=matricula)
        data = payload.model_dump(exclude_unset=True)
        if "curso_id" in data:
            await _ensure_exists(Curso, id=data["curso_id"])
        for k, v in data.items():
            setattr(obj, k, v)
        await obj.save()
        return obj

    @staticmethod
    async def delete(matricula: int) -> None:
        obj = await _ensure_exists(Aluno, matricula=matricula)
        await obj.delete()

    @staticmethod
    async def get(matricula: int) -> Aluno:
        return await _ensure_exists(Aluno, matricula=matricula)

    @staticmethod
    async def list_all():
        return await Aluno.all().prefetch_related("curso")

    @staticmethod
    async def list_paginated(limit: int = 10, offset: int = 0):
        """
        Retorna (rows, total) para paginação.
        """
        qs = Aluno.all().offset(offset).limit(limit).prefetch_related("curso")
        rows = await qs
        total = await Aluno.all().count()
        return rows, total

    @staticmethod
    async def response(obj: Aluno) -> AlunoResponse:
        return AlunoResponse(
            matricula=obj.matricula,
            nome=obj.nome,
            total_creditos=obj.total_creditos,
            data_nascimento=obj.data_nascimento,
            mgp=obj.mgp,
            curso_id=obj.curso_id,
            curso=CursoSummary(id=obj.curso.id, nome=obj.curso.nome),
        )


# =========================
# Histórico
# =========================
class HistoricoService:
    @staticmethod
    async def create(payload: HistoricoCreate) -> Historico:
        await _ensure_exists(PeriodoLetivo, id=payload.periodo_letivo_id)
        await _ensure_exists(Aluno, matricula=payload.aluno_id)
        await _ensure_exists(Disciplina, id=payload.disciplina_id)
        exists = await Historico.get_or_none(
            periodo_letivo_id=payload.periodo_letivo_id,
            aluno_id=payload.aluno_id,
            disciplina_id=payload.disciplina_id,
        )
        if exists:
            raise HTTPException(
                status_code=409,
                detail="Histórico já existe para (PL, aluno, disciplina).",
            )
        obj = Historico(**payload.model_dump())
        await obj.save()
        return obj

    @staticmethod
    async def update(id_: int, payload: HistoricoUpdate) -> Historico:
        obj = await _ensure_exists(Historico, id=id_)
        data = payload.model_dump(exclude_unset=True)
        if "periodo_letivo_id" in data:
            await _ensure_exists(PeriodoLetivo, id=data["periodo_letivo_id"])
        if "aluno_id" in data:
            await _ensure_exists(Aluno, matricula=data["aluno_id"])
        if "disciplina_id" in data:
            await _ensure_exists(Disciplina, id=data["disciplina_id"])
        # checa unique
        pl = data.get("periodo_letivo_id", obj.periodo_letivo_id)
        al = data.get("aluno_id", obj.aluno_id)
        di = data.get("disciplina_id", obj.disciplina_id)
        other = await Historico.get_or_none(
            periodo_letivo_id=pl, aluno_id=al, disciplina_id=di
        )
        if other and other.id != obj.id:
            raise HTTPException(
                status_code=409, detail="Outro Histórico já usa estes dados."
            )
        for k, v in data.items():
            setattr(obj, k, v)
        await obj.save()
        return obj

    @staticmethod
    async def delete(id_: int) -> None:
        obj = await _ensure_exists(Historico, id=id_)
        await obj.delete()

    @staticmethod
    async def get(id_: int) -> Historico:
        return await _ensure_exists(Historico, id=id_)

    @staticmethod
    async def list_all():
        return await Historico.all().prefetch_related(
            "periodo_letivo", "aluno", "disciplina"
        )

    @staticmethod
    async def response(obj: Historico) -> HistoricoResponse:
        return HistoricoResponse(
            id=obj.id,
            periodo_letivo_id=obj.periodo_letivo_id,
            aluno_id=obj.aluno_id,
            disciplina_id=obj.disciplina_id,
            situacao=obj.situacao,
            media_final=obj.media_final,
            faltas=obj.faltas,
            periodo_letivo=PeriodoLetivoSummary(
                id=obj.periodo_letivo.id,
                ano=obj.periodo_letivo.ano,
                semestre=obj.periodo_letivo.semestre,
            ),
            aluno=AlunoSummary(matricula=obj.aluno.matricula, nome=obj.aluno.nome),
            disciplina=DisciplinaSummary(
                id=obj.disciplina.id,
                nome=obj.disciplina.nome,
                creditos=obj.disciplina.creditos,
            ),
        )


# =========================
# Matrícula (lançamentos por turma)
# =========================
class MatriculaService:
    @staticmethod
    async def create(payload: MatriculaCreate) -> Matricula:
        await _ensure_exists(Aluno, matricula=payload.aluno_id)
        await _ensure_exists(Turma, id=payload.turma_id)
        exists = await Matricula.get_or_none(
            aluno_id=payload.aluno_id, turma_id=payload.turma_id
        )
        if exists:
            raise HTTPException(
                status_code=409, detail="Aluno já matriculado nesta Turma."
            )
        obj = Matricula(**payload.model_dump())
        await obj.save()
        return obj

    @staticmethod
    async def update(id_: int, payload: MatriculaUpdate) -> Matricula:
        obj = await _ensure_exists(Matricula, id=id_)
        data = payload.model_dump(exclude_unset=True)
        if "aluno_id" in data:
            await _ensure_exists(Aluno, matricula=data["aluno_id"])
        if "turma_id" in data:
            await _ensure_exists(Turma, id=data["turma_id"])
        # checa unique
        al = data.get("aluno_id", obj.aluno_id)
        tu = data.get("turma_id", obj.turma_id)
        other = await Matricula.get_or_none(aluno_id=al, turma_id=tu)
        if other and other.id != obj.id:
            raise HTTPException(
                status_code=409, detail="Já existe outra Matrícula com estes dados."
            )
        for k, v in data.items():
            setattr(obj, k, v)
        await obj.save()
        return obj

    @staticmethod
    async def delete(id_: int) -> None:
        obj = await _ensure_exists(Matricula, id=id_)
        await obj.delete()

    @staticmethod
    async def get(id_: int) -> Matricula:
        return await _ensure_exists(Matricula, id=id_)

    @staticmethod
    async def list_all():
        return await Matricula.all().prefetch_related("aluno", "turma")

    @staticmethod
    async def response(obj: Matricula) -> MatriculaResponse:
        return MatriculaResponse(
            id=obj.id,
            aluno_id=obj.aluno_id,
            turma_id=obj.turma_id,
            nota_01=obj.nota_01,
            nota_02=obj.nota_02,
            nota_03=obj.nota_03,
            faltas_01=obj.faltas_01,
            faltas_02=obj.faltas_02,
            faltas_03=obj.faltas_03,
            aluno=AlunoSummary(matricula=obj.aluno.matricula, nome=obj.aluno.nome),
            turma=TurmaSummary(id=obj.turma.id, vagas=obj.turma.vagas),
        )

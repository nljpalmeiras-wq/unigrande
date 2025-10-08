# app/schemas/unigrande.py
from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict


# =========================
# Helpers (resumos p/ leitura)
# =========================
class CursoSummary(BaseModel):
    id: int
    nome: str
    model_config = ConfigDict(from_attributes=True)


class ProfessorSummary(BaseModel):
    id: int
    nome: str
    model_config = ConfigDict(from_attributes=True)


class DisciplinaSummary(BaseModel):
    id: int
    nome: str
    creditos: int
    model_config = ConfigDict(from_attributes=True)


class PeriodoLetivoSummary(BaseModel):
    id: int
    ano: int
    semestre: int
    model_config = ConfigDict(from_attributes=True)


class AlunoSummary(BaseModel):
    matricula: int
    nome: str
    model_config = ConfigDict(from_attributes=True)


class TurmaSummary(BaseModel):
    id: int
    vagas: int
    model_config = ConfigDict(from_attributes=True)


# =========================
# PeriodoLetivo
# =========================
class PeriodoLetivoBase(BaseModel):
    ano: int
    semestre: int  # 1 ou 2
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None


class PeriodoLetivoCreate(PeriodoLetivoBase):
    pass


class PeriodoLetivoUpdate(BaseModel):
    ano: Optional[int] = None
    semestre: Optional[int] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None


class PeriodoLetivoResponse(PeriodoLetivoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# =========================
# Curso
# =========================
class CursoBase(BaseModel):
    nome: str
    total_creditos: int
    coordenador_id: Optional[int] = None  # Professor.id (idt_prof)


class CursoCreate(CursoBase):
    id: int  # cod_curso (PK definida manualmente)


class CursoUpdate(BaseModel):
    nome: Optional[str] = None
    total_creditos: Optional[int] = None
    coordenador_id: Optional[int] = None


class CursoResponse(CursoBase):
    id: int
    coordenador: Optional[ProfessorSummary] = None
    model_config = ConfigDict(from_attributes=True)


# =========================
# Professor
# =========================
class ProfessorBase(BaseModel):
    matricula: Optional[int] = None  # mat_prof
    nome: str


class ProfessorCreate(ProfessorBase):
    id: int  # idt_prof


class ProfessorUpdate(BaseModel):
    matricula: Optional[int] = None
    nome: Optional[str] = None


class ProfessorResponse(ProfessorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# =========================
# Disciplina
# =========================
class DisciplinaBase(BaseModel):
    nome: str
    creditos: int
    tipo: str  # 'O', 'E', etc.
    horas_obrig: int
    limite_faltas: int


class DisciplinaCreate(DisciplinaBase):
    id: int  # cod_disc


class DisciplinaUpdate(BaseModel):
    nome: Optional[str] = None
    creditos: Optional[int] = None
    tipo: Optional[str] = None
    horas_obrig: Optional[int] = None
    limite_faltas: Optional[int] = None


class DisciplinaResponse(DisciplinaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# =========================
# Matriz (currículo)
# =========================
class MatrizBase(BaseModel):
    curso_id: int
    disciplina_id: int
    periodo: int  # período/semestre no currículo


class MatrizCreate(MatrizBase):
    id: int


class MatrizUpdate(BaseModel):
    curso_id: Optional[int] = None
    disciplina_id: Optional[int] = None
    periodo: Optional[int] = None


class MatrizResponse(MatrizBase):
    id: int
    curso: CursoSummary
    disciplina: DisciplinaSummary
    model_config = ConfigDict(from_attributes=True)


# =========================
# Turma (oferta)
# =========================
class TurmaBase(BaseModel):
    periodo_letivo_id: int
    curso_id: int
    disciplina_id: int
    professor_id: Optional[int] = None
    vagas: int = 0


class TurmaCreate(TurmaBase):
    id: int


class TurmaUpdate(BaseModel):
    periodo_letivo_id: Optional[int] = None
    curso_id: Optional[int] = None
    disciplina_id: Optional[int] = None
    professor_id: Optional[int] = None
    vagas: Optional[int] = None


class TurmaResponse(TurmaBase):
    id: int
    periodo_letivo: PeriodoLetivoSummary
    curso: CursoSummary
    disciplina: DisciplinaSummary
    professor: Optional[ProfessorSummary] = None
    model_config = ConfigDict(from_attributes=True)


# =========================
# Aluno
# =========================
class AlunoBase(BaseModel):
    nome: str
    total_creditos: int
    data_nascimento: Optional[date] = None
    mgp: Optional[Decimal] = None
    curso_id: int


class AlunoCreate(AlunoBase):
    matricula: int  # PK


class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    total_creditos: Optional[int] = None
    data_nascimento: Optional[date] = None
    mgp: Optional[Decimal] = None
    curso_id: Optional[int] = None


class AlunoResponse(AlunoBase):
    matricula: int
    curso: CursoSummary
    model_config = ConfigDict(from_attributes=True)


# =========================
# Histórico (resultado final por PL/disciplina)
# =========================
SituacaoLiteral = Literal["AP", "RE", "TC", "MT"]  # ajuste livre conforme regras


class HistoricoBase(BaseModel):
    periodo_letivo_id: int
    aluno_id: int  # referencia a Aluno.matricula
    disciplina_id: int
    situacao: SituacaoLiteral
    media_final: Optional[Decimal] = None
    faltas: Optional[int] = None


class HistoricoCreate(HistoricoBase):
    id: int


class HistoricoUpdate(BaseModel):
    periodo_letivo_id: Optional[int] = None
    aluno_id: Optional[int] = None
    disciplina_id: Optional[int] = None
    situacao: Optional[SituacaoLiteral] = None
    media_final: Optional[Decimal] = None
    faltas: Optional[int] = None


class HistoricoResponse(HistoricoBase):
    id: int
    periodo_letivo: PeriodoLetivoSummary
    aluno: AlunoSummary
    disciplina: DisciplinaSummary
    model_config = ConfigDict(from_attributes=True)


# =========================
# Matrícula (lançamentos por turma)
# =========================
class MatriculaBase(BaseModel):
    aluno_id: int  # Aluno.matricula
    turma_id: int
    nota_01: Optional[Decimal] = None
    nota_02: Optional[Decimal] = None
    nota_03: Optional[Decimal] = None
    faltas_01: Optional[int] = None
    faltas_02: Optional[int] = None
    faltas_03: Optional[int] = None


class MatriculaCreate(MatriculaBase):
    id: int


class MatriculaUpdate(BaseModel):
    aluno_id: Optional[int] = None
    turma_id: Optional[int] = None
    nota_01: Optional[Decimal] = None
    nota_02: Optional[Decimal] = None
    nota_03: Optional[Decimal] = None
    faltas_01: Optional[int] = None
    faltas_02: Optional[int] = None
    faltas_03: Optional[int] = None


class MatriculaResponse(MatriculaBase):
    id: int
    aluno: AlunoSummary
    turma: TurmaSummary
    model_config = ConfigDict(from_attributes=True)

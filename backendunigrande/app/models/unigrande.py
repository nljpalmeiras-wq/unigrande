from tortoise import fields, models


# --------- TABELAS DE APOIO ---------
class PeriodoLetivo(models.Model):
    """
    PERIODOS_LETIVOS
    """

    id = fields.IntField(pk=True)
    ano = fields.IntField()
    semestre = fields.IntField()  # 1 ou 2
    data_inicio = fields.DateField(null=True)
    data_fim = fields.DateField(null=True)

    class Meta:
        table = "periodos_letivos"
        unique_together = (("ano", "semestre"),)
        indexes = (("ano", "semestre"),)

    def __str__(self) -> str:
        return f"{self.ano}.{self.semestre}"


class Curso(models.Model):
    """
    CURSOS
    """

    id = fields.IntField(pk=True)  # cod_curso
    nome = fields.CharField(max_length=40)
    total_creditos = fields.IntField()
    coordenador = fields.ForeignKeyField(
        "models.Professor",
        related_name="cursos_coordenados",
        null=True,  # pode não existir ainda
        on_delete=fields.CASCADE,
        source_field="idt_prof",  # mantém a ideia do ER
    )

    class Meta:
        table = "cursos"
        indexes = ("nome",)


class Professor(models.Model):
    """
    PROFESSORES
    """

    id = fields.IntField(pk=True)  # idt_prof
    matricula = fields.IntField(null=True)  # mat_prof
    nome = fields.CharField(max_length=50)

    class Meta:
        table = "professores"
        indexes = ("nome",)


class Disciplina(models.Model):
    """
    DISCIPLINAS
    """

    id = fields.IntField(pk=True)  # cod_disc
    nome = fields.CharField(max_length=50)
    creditos = fields.IntField()
    tipo = fields.CharField(max_length=1)  # 'O' obrigatória, 'E' eletiva, etc.
    horas_obrig = fields.IntField()
    limite_faltas = fields.IntField()

    class Meta:
        table = "disciplinas"
        indexes = ("nome",)


class Matriz(models.Model):
    """
    MATRIZES = currículo (qual disciplina pertence a qual curso e em qual período)
    """

    id = fields.IntField(pk=True)
    curso = fields.ForeignKeyField("models.Curso", related_name="matrizes")
    disciplina = fields.ForeignKeyField("models.Disciplina", related_name="matrizes")
    periodo = fields.IntField()  # período/semestre no currículo

    class Meta:
        table = "matrizes"
        unique_together = (("curso", "disciplina"),)
        indexes = (("curso_id", "periodo"),)


class Turma(models.Model):
    """
    TURMAS (oferta da disciplina no período letivo, com professor e vagas)
    """

    id = fields.IntField(pk=True)
    periodo_letivo = fields.ForeignKeyField(
        "models.PeriodoLetivo", related_name="turmas"
    )
    curso = fields.ForeignKeyField("models.Curso", related_name="turmas")
    disciplina = fields.ForeignKeyField("models.Disciplina", related_name="turmas")
    professor = fields.ForeignKeyField(
        "models.Professor", related_name="turmas", null=True
    )
    vagas = fields.IntField(default=0)

    class Meta:
        table = "turmas"
        # evita duplicar oferta da mesma disciplina no mesmo PL/curso
        unique_together = (("periodo_letivo", "curso", "disciplina"),)
        indexes = (("periodo_letivo_id", "curso_id"),)


# --------- ALUNOS, HISTÓRICO, MATRÍCULAS ---------
class Aluno(models.Model):
    """
    ALUNOS
    """

    matricula = fields.IntField(pk=True)  # mat_alu
    nome = fields.CharField(max_length=50)
    total_creditos = fields.IntField()
    data_nascimento = fields.DateField(null=True)
    mgp = fields.DecimalField(max_digits=5, decimal_places=2, null=True)
    curso = fields.ForeignKeyField("models.Curso", related_name="alunos")

    class Meta:
        table = "alunos"
        indexes = ("nome", "curso_id")


class Historico(models.Model):
    """
    HISTORICOS (resultado final do aluno em uma disciplina em um ano/semestre)
    """

    id = fields.IntField(pk=True)
    periodo_letivo = fields.ForeignKeyField(
        "models.PeriodoLetivo", related_name="historicos"
    )
    aluno = fields.ForeignKeyField("models.Aluno", related_name="historicos")
    disciplina = fields.ForeignKeyField("models.Disciplina", related_name="historicos")
    situacao = fields.CharField(max_length=2)  # AP/RE/TC/MT, etc.
    media_final = fields.DecimalField(max_digits=5, decimal_places=2, null=True)
    faltas = fields.IntField(null=True)

    class Meta:
        table = "historicos"
        unique_together = (("periodo_letivo", "aluno", "disciplina"),)
        indexes = (("aluno_id", "periodo_letivo_id"),)


class Matricula(models.Model):
    """
    MATRICULAS (lançamentos de avaliações e faltas por oferta/Turma)
    """

    id = fields.IntField(pk=True)
    aluno = fields.ForeignKeyField("models.Aluno", related_name="matriculas")
    turma = fields.ForeignKeyField("models.Turma", related_name="matriculas")

    # Notas (até 3 avaliações) e faltas por avaliação
    nota_01 = fields.DecimalField(max_digits=5, decimal_places=2, null=True)
    nota_02 = fields.DecimalField(max_digits=5, decimal_places=2, null=True)
    nota_03 = fields.DecimalField(max_digits=5, decimal_places=2, null=True)
    faltas_01 = fields.IntField(null=True)
    faltas_02 = fields.IntField(null=True)
    faltas_03 = fields.IntField(null=True)

    class Meta:
        table = "matriculas"
        unique_together = (("aluno", "turma"),)
        indexes = (("aluno_id", "turma_id"),)

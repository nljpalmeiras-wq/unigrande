from tortoise import fields, models

class PeriodoLetivo(models.Model):
    id = fields.IntField(pk=True)
    ano = fields.IntField() # ano que pode ser 2020, 2025
    semestre = fields.IntField() # semestre que pode ser 1 ou 2
    data_inicio = fields.DateField()
    data_fim = fields.DateField()

    class Meta:
        table = "periodos_letivos"
        unique_together = (("ano", "semestre"),)
        indexes = (("ano", "semestre"),)

class Professor(models.Model):
    pass

class Curso(models.Model):
    pass

class Disciplina(models.Model):
    pass

class Matriz(models.Model):
    pass

class Turma(models.Model):
    pass

class Aluno(models.Model):
    pass

class Matricula(models.Model):
    pass

class Historico(models.Model):
    pass
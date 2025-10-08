from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "disciplinas" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "nome" VARCHAR(50) NOT NULL,
    "creditos" INT NOT NULL,
    "tipo" VARCHAR(1) NOT NULL,
    "horas_obrig" INT NOT NULL,
    "limite_faltas" INT NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_disciplinas_nome_772c8d" ON "disciplinas" ("nome");
COMMENT ON TABLE "disciplinas" IS 'DISCIPLINAS';
CREATE TABLE IF NOT EXISTS "periodos_letivos" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "ano" INT NOT NULL,
    "semestre" INT NOT NULL,
    "data_inicio" DATE,
    "data_fim" DATE,
    CONSTRAINT "uid_periodos_le_ano_ac5cb8" UNIQUE ("ano", "semestre")
);
CREATE INDEX IF NOT EXISTS "idx_periodos_le_ano_ac5cb8" ON "periodos_letivos" ("ano", "semestre");
COMMENT ON TABLE "periodos_letivos" IS 'PERIODOS_LETIVOS';
CREATE TABLE IF NOT EXISTS "professores" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "matricula" INT,
    "nome" VARCHAR(50) NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_professores_nome_cd2569" ON "professores" ("nome");
COMMENT ON TABLE "professores" IS 'PROFESSORES';
CREATE TABLE IF NOT EXISTS "cursos" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "nome" VARCHAR(40) NOT NULL,
    "total_creditos" INT NOT NULL,
    "coordenador_id" INT REFERENCES "professores" ("id") ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS "idx_cursos_nome_7ce005" ON "cursos" ("nome");
COMMENT ON TABLE "cursos" IS 'CURSOS';
CREATE TABLE IF NOT EXISTS "alunos" (
    "matricula" SERIAL NOT NULL PRIMARY KEY,
    "nome" VARCHAR(50) NOT NULL,
    "total_creditos" INT NOT NULL,
    "data_nascimento" DATE,
    "mgp" DECIMAL(5,2),
    "curso_id" INT NOT NULL REFERENCES "cursos" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_alunos_nome_a02d79" ON "alunos" ("nome", "curso_id");
COMMENT ON TABLE "alunos" IS 'ALUNOS';
CREATE TABLE IF NOT EXISTS "historicos" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "situacao" VARCHAR(2) NOT NULL,
    "media_final" DECIMAL(5,2),
    "faltas" INT,
    "aluno_id" INT NOT NULL REFERENCES "alunos" ("matricula") ON DELETE CASCADE,
    "disciplina_id" INT NOT NULL REFERENCES "disciplinas" ("id") ON DELETE CASCADE,
    "periodo_letivo_id" INT NOT NULL REFERENCES "periodos_letivos" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_historicos_periodo_d773b3" UNIQUE ("periodo_letivo_id", "aluno_id", "disciplina_id")
);
CREATE INDEX IF NOT EXISTS "idx_historicos_aluno_i_33943e" ON "historicos" ("aluno_id", "periodo_letivo_id");
COMMENT ON TABLE "historicos" IS 'HISTORICOS (resultado final do aluno em uma disciplina em um ano/semestre)';
CREATE TABLE IF NOT EXISTS "matrizes" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "periodo" INT NOT NULL,
    "curso_id" INT NOT NULL REFERENCES "cursos" ("id") ON DELETE CASCADE,
    "disciplina_id" INT NOT NULL REFERENCES "disciplinas" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_matrizes_curso_i_c01d41" UNIQUE ("curso_id", "disciplina_id")
);
CREATE INDEX IF NOT EXISTS "idx_matrizes_curso_i_ae9427" ON "matrizes" ("curso_id", "periodo");
COMMENT ON TABLE "matrizes" IS 'MATRIZES = currículo (qual disciplina pertence a qual curso e em qual período)';
CREATE TABLE IF NOT EXISTS "turmas" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "vagas" INT NOT NULL DEFAULT 0,
    "curso_id" INT NOT NULL REFERENCES "cursos" ("id") ON DELETE CASCADE,
    "disciplina_id" INT NOT NULL REFERENCES "disciplinas" ("id") ON DELETE CASCADE,
    "periodo_letivo_id" INT NOT NULL REFERENCES "periodos_letivos" ("id") ON DELETE CASCADE,
    "professor_id" INT REFERENCES "professores" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_turmas_periodo_3c0e08" UNIQUE ("periodo_letivo_id", "curso_id", "disciplina_id")
);
CREATE INDEX IF NOT EXISTS "idx_turmas_periodo_2867d7" ON "turmas" ("periodo_letivo_id", "curso_id");
COMMENT ON TABLE "turmas" IS 'TURMAS (oferta da disciplina no período letivo, com professor e vagas)';
CREATE TABLE IF NOT EXISTS "matriculas" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "nota_01" DECIMAL(5,2),
    "nota_02" DECIMAL(5,2),
    "nota_03" DECIMAL(5,2),
    "faltas_01" INT,
    "faltas_02" INT,
    "faltas_03" INT,
    "aluno_id" INT NOT NULL REFERENCES "alunos" ("matricula") ON DELETE CASCADE,
    "turma_id" INT NOT NULL REFERENCES "turmas" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_matriculas_aluno_i_f30770" UNIQUE ("aluno_id", "turma_id")
);
CREATE INDEX IF NOT EXISTS "idx_matriculas_aluno_i_f30770" ON "matriculas" ("aluno_id", "turma_id");
COMMENT ON TABLE "matriculas" IS 'MATRICULAS (lançamentos de avaliações e faltas por oferta/Turma)';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """

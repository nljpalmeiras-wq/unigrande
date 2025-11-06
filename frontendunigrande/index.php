<?php
// Ajuste essa URL para o endereço real da sua API FastAPI
// Ex: "http://localhost:8000" ou "https://sua-api.com/unigrande"
$API_BASE_URL = "http://backendunigrande:5000";
?>

<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8" />
    <title>CRUD de Alunos - Unigrande</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <style>
        :root {
            --primary: #2563eb;
            --primary-dark: #1d4ed8;
            --danger: #dc2626;
            --bg: #f3f4f6;
            --card-bg: #ffffff;
            --border: #e5e7eb;
            --text-main: #111827;
            --text-muted: #6b7280;
        }

        * {
            box-sizing: border-box;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        body {
            margin: 0;
            padding: 20px;
            background: var(--bg);
            color: var(--text-main);
        }

        h1 {
            margin-top: 0;
            margin-bottom: 10px;
        }

        .page-container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .card {
            background: var(--card-bg);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 10px 20px rgba(15, 23, 42, 0.05);
            border: 1px solid var(--border);
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            gap: 10px;
            flex-wrap: wrap;
        }

        .card-header h2 {
            margin: 0;
            font-size: 1.1rem;
        }

        .card-header small {
            color: var(--text-muted);
        }

        label {
            display: block;
            font-size: 0.9rem;
            margin-bottom: 4px;
            color: var(--text-muted);
        }

        input {
            width: 100%;
            padding: 8px 10px;
            border-radius: 6px;
            border: 1px solid var(--border);
            outline: none;
            font-size: 0.95rem;
        }

        input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 1px rgba(37, 99, 235, 0.2);
        }

        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 12px 16px;
        }

        .btn {
            border: none;
            border-radius: 999px;
            padding: 8px 16px;
            font-size: 0.9rem;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            white-space: nowrap;
        }

        .btn-primary {
            background: var(--primary);
            color: #fff;
        }

        .btn-primary:hover {
            background: var(--primary-dark);
        }

        .btn-outline {
            background: transparent;
            border: 1px solid var(--border);
            color: var(--text-main);
        }

        .btn-outline:hover {
            background: #f9fafb;
        }

        .btn-danger {
            background: var(--danger);
            color: #fff;
        }

        .btn-danger:hover {
            background: #b91c1c;
        }

        .btn-sm {
            padding: 4px 10px;
            font-size: 0.8rem;
        }

        .actions-row {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }

        .message {
            margin-top: 10px;
            padding: 8px 10px;
            border-radius: 6px;
            font-size: 0.85rem;
        }

        .message.info {
            background: #eff6ff;
            color: #1d4ed8;
        }

        .message.error {
            background: #fef2f2;
            color: #b91c1c;
        }

        .message.success {
            background: #ecfdf5;
            color: #15803d;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }

        thead {
            background: #f9fafb;
        }

        th, td {
            padding: 8px 10px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }

        th {
            font-weight: 600;
            color: var(--text-muted);
            font-size: 0.8rem;
            text-transform: uppercase;
        }

        tr:hover td {
            background: #f9fafb;
        }

        .badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 999px;
            font-size: 0.75rem;
            background: #eff6ff;
            color: #1d4ed8;
        }

        .table-actions {
            display: flex;
            gap: 6px;
        }

        .search-inline {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: center;
        }

        .search-inline input {
            max-width: 200px;
        }

        @media (max-width: 768px) {
            .card-header {
                align-items: flex-start;
            }
        }
    </style>
</head>
<body>
<div class="page-container">
    <h1>CRUD de Alunos</h1>
    <p style="color: var(--text-muted); margin-top: 0;">
        Integração com API FastAPI (<code>/create-aluno</code>, <code>/listar-alunos</code>, <code>/buscar-aluno</code>, <code>/atualizar-aluno</code>, <code>/delete-aluno</code>).
    </p>

    <!-- CARD: Formulário de cadastro/edição -->
    <div class="card">
        <div class="card-header">
            <div>
                <h2 id="form-title">Cadastrar novo aluno</h2>
                <small id="form-subtitle">Preencha os dados e clique em "Salvar aluno".</small>
            </div>
            <button type="button" class="btn btn-outline" id="btn-clear-form">Limpar formulário</button>
        </div>

        <div class="form-grid">
            <div>
                <label for="matricula">Matrícula (PK / path)</label>
                <input type="number" id="matricula" placeholder="Ex: 20241234" />
            </div>
            <div>
                <label for="nome">Nome</label>
                <input type="text" id="nome" placeholder="Nome do aluno" />
            </div>
            <div>
                <label for="email">E-mail</label>
                <input type="email" id="email" placeholder="email@exemplo.com" />
            </div>
            <div>
                <label for="curso_id">Curso ID (FK)</label>
                <input type="number" id="curso_id" placeholder="ID do curso" />
            </div>
        </div>

        <div class="actions-row">
            <button type="button" class="btn btn-primary" id="btn-save-aluno">
                💾 Salvar aluno
            </button>
            <button type="button" class="btn btn-outline" id="btn-update-aluno">
                ✏️ Atualizar aluno (pela matrícula)
            </button>
        </div>

        <div id="form-message" class="message" style="display:none;"></div>
    </div>

    <!-- CARD: Buscar por matrícula -->
    <div class="card">
        <div class="card-header">
            <div>
                <h2>Buscar aluno por matrícula</h2>
                <small>Usa o endpoint <code>GET /buscar-aluno/{matricula}</code>.</small>
            </div>
        </div>

        <div class="search-inline">
            <input type="number" id="search-matricula" placeholder="Matrícula" />
            <button type="button" class="btn btn-outline" id="btn-search-aluno">
                🔍 Buscar
            </button>
        </div>

        <div id="search-message" class="message" style="display:none; margin-top: 10px;"></div>
    </div>

    <!-- CARD: Lista de alunos -->
    <div class="card">
        <div class="card-header">
            <div>
                <h2>Lista de alunos</h2>
                <small>Carrega os dados de <code>GET /listar-alunos</code>.</small>
            </div>
            <button type="button" class="btn btn-outline" id="btn-refresh-list">
                🔄 Atualizar lista
            </button>
        </div>

        <div style="overflow-x:auto;">
            <table>
                <thead>
                <tr>
                    <th>Matrícula</th>
                    <th>Nome</th>
                    <th>E-mail</th>
                    <th>Curso ID</th>
                    <th>Ações</th>
                </tr>
                </thead>
                <tbody id="alunos-tbody">
                <tr>
                    <td colspan="5" style="text-align:center; color: var(--text-muted);">
                        Nenhum aluno carregado ainda. Clique em "Atualizar lista".
                    </td>
                </tr>
                </tbody>
            </table>
        </div>

        <div id="list-message" class="message" style="display:none; margin-top: 10px;"></div>
    </div>
</div>

<script>
    const API_BASE_URL = "<?php echo $API_BASE_URL; ?>";

    const endpoints = {
        createAluno: () => `${API_BASE_URL}/alunos/create-aluno`,
        listAlunos: () => `${API_BASE_URL}/listar-alunos`,
        getAluno: (matricula) => `${API_BASE_URL}/buscar-aluno/${matricula}`,
        updateAluno: (matricula) => `${API_BASE_URL}/atualizar-aluno/${matricula}`,
        deleteAluno: (matricula) => `${API_BASE_URL}/delete-aluno/${matricula}`,
    };

    // Util: mostrar mensagens
    function showMessage(el, message, type = "info") {
        el.textContent = message;
        el.className = `message ${type}`;
        el.style.display = "block";
    }

    function hideMessage(el) {
        el.style.display = "none";
    }

    // Util: pegar dados do form
    function getFormData() {
        return {
            matricula: document.getElementById("matricula").value.trim(),
            nome: document.getElementById("nome").value.trim(),
            email: document.getElementById("email").value.trim(),
            curso_id: document.getElementById("curso_id").value.trim(),
        };
    }

    // Preencher formulário a partir de um objeto aluno
    function fillForm(aluno) {
        if (!aluno) return;
        // Ajuste os nomes dos campos conforme o seu AlunoResponse
        document.getElementById("matricula").value = aluno.matricula ?? "";
        document.getElementById("nome").value = aluno.nome ?? "";
        document.getElementById("email").value = aluno.email ?? "";
        document.getElementById("curso_id").value = aluno.curso_id ?? "";

        document.getElementById("form-title").textContent = "Editar aluno";
        document.getElementById("form-subtitle").textContent = "Altere os campos e clique em 'Atualizar aluno'.";
    }

    function clearForm() {
        document.getElementById("matricula").value = "";
        document.getElementById("nome").value = "";
        document.getElementById("email").value = "";
        document.getElementById("curso_id").value = "";
        document.getElementById("form-title").textContent = "Cadastrar novo aluno";
        document.getElementById("form-subtitle").textContent = "Preencha os dados e clique em 'Salvar aluno'.";
    }

    // ==========================
    // CREATE
    // ==========================
    async function createAluno() {
        const formMsg = document.getElementById("form-message");
        hideMessage(formMsg);

        const data = getFormData();

        // Monte o payload conforme o seu AlunoCreate
        const payload = {
            // Se a matrícula for gerada pela API, remova daqui
            matricula: data.matricula ? Number(data.matricula) : undefined,
            nome: data.nome,
            email: data.email,
            curso_id: data.curso_id ? Number(data.curso_id) : null,
        };

        if (!payload.nome || !payload.email) {
            showMessage(formMsg, "Nome e e-mail são obrigatórios.", "error");
            return;
        }

        try {
            showMessage(formMsg, "Salvando aluno...", "info");

            const res = await fetch(endpoints.createAluno(), {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(payload),
            });

            const resData = res.status !== 204 ? await res.json().catch(() => null) : null;

            if (!res.ok) {
                const detail = resData?.detail || `Erro ${res.status}`;
                showMessage(formMsg, `Erro ao criar aluno: ${detail}`, "error");
                return;
            }

            showMessage(formMsg, "Aluno criado com sucesso!", "success");
            fillForm(resData);     // já preenche com o retorno da API
            await loadAlunos();    // atualiza a lista
        } catch (e) {
            console.error(e);
            showMessage(formMsg, "Erro inesperado ao criar aluno.", "error");
        }
    }

    // ==========================
    // LIST
    // ==========================
    async function loadAlunos() {
        const listMsg = document.getElementById("list-message");
        const tbody = document.getElementById("alunos-tbody");
        hideMessage(listMsg);

        tbody.innerHTML = `
            <tr>
                <td colspan="5" style="text-align:center; color: var(--text-muted);">
                    Carregando alunos...
                </td>
            </tr>
        `;

        try {
            const res = await fetch(endpoints.listAlunos());
            const data = await res.json();

            if (!res.ok) {
                const detail = data?.detail || `Erro ${res.status}`;
                showMessage(listMsg, `Erro ao listar alunos: ${detail}`, "error");
                return;
            }

            if (!Array.isArray(data) || data.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="5" style="text-align:center; color: var(--text-muted);">
                            Nenhum aluno encontrado.
                        </td>
                    </tr>
                `;
                return;
            }

            tbody.innerHTML = "";
            data.forEach(aluno => {
                const tr = document.createElement("tr");

                // Ajuste os nomes das propriedades conforme AlunoResponse
                const matricula = aluno.matricula ?? "";
                const nome = aluno.nome ?? "";
                const email = aluno.email ?? "";
                const cursoId = aluno.curso_id ?? "";

                tr.innerHTML = `
                    <td><span class="badge">${matricula}</span></td>
                    <td>${nome}</td>
                    <td>${email}</td>
                    <td>${cursoId}</td>
                    <td>
                        <div class="table-actions">
                            <button type="button" class="btn btn-outline btn-sm" data-action="edit">
                                ✏️ Editar
                            </button>
                            <button type="button" class="btn btn-danger btn-sm" data-action="delete">
                                🗑️ Excluir
                            </button>
                        </div>
                    </td>
                `;

                // Eventos dos botões
                tr.querySelector('[data-action="edit"]').addEventListener("click", () => {
                    fillForm(aluno);
                    document.getElementById("search-matricula").value = matricula;
                });

                tr.querySelector('[data-action="delete"]').addEventListener("click", () => {
                    if (confirm(`Tem certeza que deseja excluir o aluno de matrícula ${matricula}?`)) {
                        deleteAluno(matricula);
                    }
                });

                tbody.appendChild(tr);
            });
        } catch (e) {
            console.error(e);
            showMessage(listMsg, "Erro inesperado ao carregar alunos.", "error");
        }
    }

    // ==========================
    // GET por matrícula
    // ==========================
    async function buscarAlunoPorMatricula() {
        const searchMsg = document.getElementById("search-message");
        hideMessage(searchMsg);

        const matricula = document.getElementById("search-matricula").value.trim();

        if (!matricula) {
            showMessage(searchMsg, "Informe uma matrícula para buscar.", "error");
            return;
        }

        try {
            showMessage(searchMsg, "Buscando aluno...", "info");

            const res = await fetch(endpoints.getAluno(matricula));
            const data = await res.json().catch(() => null);

            if (!res.ok) {
                const detail = data?.detail || `Erro ${res.status}`;
                showMessage(searchMsg, `Erro ao buscar aluno: ${detail}`, "error");
                return;
            }

            showMessage(searchMsg, `Aluno encontrado: ${data.nome} (curso ${data.curso_id})`, "success");
            fillForm(data);
        } catch (e) {
            console.error(e);
            showMessage(searchMsg, "Erro inesperado ao buscar aluno.", "error");
        }
    }

    // ==========================
    // UPDATE
    // ==========================
    async function updateAluno() {
        const formMsg = document.getElementById("form-message");
        hideMessage(formMsg);

        const data = getFormData();

        if (!data.matricula) {
            showMessage(formMsg, "Informe a matrícula do aluno que será atualizado.", "error");
            return;
        }

        const payload = {
            // Em AlunoUpdate, deixe apenas campos que podem ser alterados
            nome: data.nome || undefined,
            email: data.email || undefined,
            curso_id: data.curso_id ? Number(data.curso_id) : undefined,
        };

        try {
            showMessage(formMsg, "Atualizando aluno...", "info");

            const res = await fetch(endpoints.updateAluno(data.matricula), {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(payload),
            });

            const resData = await res.json().catch(() => null);

            if (!res.ok) {
                const detail = resData?.detail || `Erro ${res.status}`;
                showMessage(formMsg, `Erro ao atualizar aluno: ${detail}`, "error");
                return;
            }

            showMessage(formMsg, "Aluno atualizado com sucesso!", "success");
            fillForm(resData);
            await loadAlunos();
        } catch (e) {
            console.error(e);
            showMessage(formMsg, "Erro inesperado ao atualizar aluno.", "error");
        }
    }

    // ==========================
    // DELETE
    // ==========================
    async function deleteAluno(matricula) {
        const listMsg = document.getElementById("list-message");
        hideMessage(listMsg);

        if (!matricula) {
            showMessage(listMsg, "Matrícula inválida para exclusão.", "error");
            return;
        }

        try {
            showMessage(listMsg, `Excluindo aluno ${matricula}...`, "info");

            const res = await fetch(endpoints.deleteAluno(matricula), {
                method: "DELETE",
            });

            if (!res.ok && res.status !== 204) {
                const data = await res.json().catch(() => null);
                const detail = data?.detail || `Erro ${res.status}`;
                showMessage(listMsg, `Erro ao excluir aluno: ${detail}`, "error");
                return;
            }

            showMessage(listMsg, `Aluno ${matricula} excluído com sucesso.`, "success");
            await loadAlunos();
        } catch (e) {
            console.error(e);
            showMessage(listMsg, "Erro inesperado ao excluir aluno.", "error");
        }
    }

    // ==========================
    // Eventos de UI
    // ==========================
    document.addEventListener("DOMContentLoaded", () => {
        document.getElementById("btn-save-aluno").addEventListener("click", createAluno);
        document.getElementById("btn-update-aluno").addEventListener("click", updateAluno);
        document.getElementById("btn-refresh-list").addEventListener("click", loadAlunos);
        document.getElementById("btn-clear-form").addEventListener("click", () => {
            clearForm();
            hideMessage(document.getElementById("form-message"));
        });
        document.getElementById("btn-search-aluno").addEventListener("click", buscarAlunoPorMatricula);

        // Carrega a lista logo na abertura
        loadAlunos();
    });
</script>
</body>
</html>

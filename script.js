// Lógica universal para o menu hambúrguer
const hamburgerBtn = document.getElementById('hamburger-btn');
const navLinks = document.getElementById('nav-links');

if (hamburgerBtn && navLinks) {
    hamburgerBtn.addEventListener('click', () => {
        navLinks.classList.toggle('active');
    });
}

// Lógica condicional para as páginas específicas
document.addEventListener('DOMContentLoaded', () => {
    // Verifica se o formulário de login existe na página atual
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        // Lógica da página de login
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const nome = document.getElementById('nome').value;
            const cursoElement = document.getElementById('curso_select');
            const curso = cursoElement.options[cursoElement.selectedIndex].text;

            if (nome && curso && curso !== 'Selecione um curso...') {
                sessionStorage.setItem('alunoNome', nome);
                sessionStorage.setItem('alunoCurso', curso);
                window.location.href = 'demandas.html';
            } else {
                alert('Por favor, preencha todos os campos.');
            }
        });
    }

    // Verifica se a seção de demandas existe na página atual
    const demandasContainer = document.querySelector('.demandas-container');
    if (demandasContainer) {
        // Lógica da página de demandas
        const alunoNome = sessionStorage.getItem('alunoNome');
        const cursoOptionValue = sessionStorage.getItem('alunoCurso');

        if (!alunoNome || !cursoOptionValue) {
            window.location.href = 'login.html'; // Redireciona se não houver dados
            return;
        }

        document.getElementById('alunoNomeDisplay').textContent = alunoNome;
        document.getElementById('alunoCursoDisplay').textContent = cursoOptionValue;

        const demandaForm = document.getElementById('demandaForm');
        if (demandaForm) {
            demandaForm.addEventListener('submit', function(event) {
                event.preventDefault();

                const tipo = document.getElementById('tipoDemanda').value;
                const titulo = document.getElementById('titulo').value;
                const descricao = document.getElementById('descricao').value;

                alert(`Demanda enviada com sucesso!\n\nTipo: ${tipo}\nTítulo: ${titulo}\nDescrição: ${descricao}\n\nObrigado por sua colaboração, ${alunoNome}!`);
                this.reset();
            });
        }

        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => {
                sessionStorage.clear();
                window.location.href = 'login.html';
            });
        }
    }
});
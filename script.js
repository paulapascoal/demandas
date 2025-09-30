const hamburgerBtn = document.getElementById('hamburger-btn');
const navLinks = document.getElementById('nav-links');
if (hamburgerBtn && navLinks) {
    hamburgerBtn.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        const isExpanded = navLinks.classList.contains('active');
        hamburgerBtn.setAttribute('aria-expanded', isExpanded);
    });
}
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
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
    const demandasContainer = document.querySelector('.demandas-container');
    if (demandasContainer) {
        const alunoNome = sessionStorage.getItem('alunoNome');
        const cursoOptionValue = sessionStorage.getItem('alunoCurso');
        if (!alunoNome || !cursoOptionValue) {
            window.location.href = 'login.html';
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
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const nome = document.getElementById('nome').value.trim();
            const email = document.getElementById('email').value.trim();
            const mensagem = document.getElementById('mensagem').value.trim();
            if (nome === '' || email === '' || mensagem === '') {
                alert('Por favor, preencha todos os campos do formulário.');
                return;
            }
            const dadosDaDuvida = {
                nome: nome,
                email: email,
                mensagem: mensagem,
                dataEnvio: new Date().toLocaleString()
            };
            console.log('Dúvida enviada:', dadosDaDuvida);
            alert('Sua dúvida foi enviada com sucesso! Em breve entraremos em contato.');
            contactForm.reset();
        });
    }
});
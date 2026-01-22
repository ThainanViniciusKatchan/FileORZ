const fileTypes = [
    { icon: 'ph-file-pdf', color: 'text-red-500' },
    { icon: 'ph-file-doc', color: 'text-blue-500' },
    { icon: 'ph-file-xls', color: 'text-green-500' },
    { icon: 'ph-file-ppt', color: 'text-orange-500' },
    { icon: 'ph-file-video', color: 'text-purple-500' },
    { icon: 'ph-file-audio', color: 'text-yellow-500' },
    { icon: 'ph-file-html', color: 'text-orange-600' },
    { icon: 'ph-file-css', color: 'text-blue-400' },
    { icon: 'ph-file-js', color: 'text-yellow-400' },
    { icon: 'ph-file-zip', color: 'text-gray-500' },
    { icon: 'ph-file-image', color: 'text-pink-500' },
    { icon: 'ph-brackets-curly', color: 'text-cyan-400' },
    { icon: 'ph-file-text', color: 'text-gray-400' },
];

const iconUniverse = document.getElementById('icon-universe');
const heroSection = document.getElementById('hero');

function random(min, max) {
    return Math.random() * (max - min) + min;
}

// Gerar Ícones de Fundo
function spawnIcons() {
    const isMobile = window.innerWidth < 768;
    // range do mouse para ativar o efeito 30 no mobile, 80 no desktop
    const count = isMobile ? 30 : 80;

    for (let i = 0; i < count; i++) {
        const type = fileTypes[Math.floor(Math.random() * fileTypes.length)];

        // Wrapper
        const wrapper = document.createElement('div');
        wrapper.className = 'icon-wrapper';

        const left = random(2, 98);
        const top = random(2, 98);
        wrapper.style.left = `${left}%`;
        wrapper.style.top = `${top}%`;

        // Animação de flutuar
        wrapper.style.animation = `float ${random(4, 8)}s ease-in-out infinite`;
        wrapper.style.animationDelay = `${random(0, 5)}s`;

        // Ícone
        const icon = document.createElement('i');
        icon.className = `ph ${type.icon} ${type.color} floating-icon`;

        // Variações visuais
        const scale = random(0.8, 1.5);
        const rot = random(-180, 180);

        // Salva a rotação original para não perder quando escalar no hover
        icon.dataset.rotation = rot;

        // Aplica rotação inicial
        icon.style.transform = `scale(${scale}) rotate(${rot}deg)`;

        wrapper.appendChild(icon);
        iconUniverse.appendChild(wrapper);
    }
}

// Efeito de Range do Mouse
function setupMouseEffect() {
    // Raio de efeito em pixels
    const effectRadius = 200;

    // Listener de movimento no body ou apenas na hero section
    // Usando requestAnimationFrame para otimizar performance
    let ticking = false;

    document.addEventListener('mousemove', (e) => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                handleMouseMove(e);
                ticking = false;
            });
            ticking = true;
        }
    });

    function handleMouseMove(e) {
        // Só funciona se estivermos no topo da página
        if (window.scrollY > window.innerHeight) return;

        const mouseX = e.clientX;
        const mouseY = e.clientY;

        // Seleciona todos os wrappers para calcular a posição
        const wrappers = document.querySelectorAll('.icon-wrapper');

        wrappers.forEach(wrapper => {
            const icon = wrapper.querySelector('.floating-icon');
            if (!icon) return;

            // Pega a posição atual do wrapper
            const rect = wrapper.getBoundingClientRect();
            const iconX = rect.left + rect.width / 2;
            const iconY = rect.top + rect.height / 2;

            // Calcula distância
            const dist = Math.hypot(mouseX - iconX, mouseY - iconY);

            // Verifica se está dentro do raio
            if (dist < effectRadius) {
                icon.classList.add('active');
                // Aplica escala + rotação original
                icon.style.transform = `scale(1.4) rotate(${icon.dataset.rotation}deg)`;
            } else {
                icon.classList.remove('active');
                // Volta ao tamanho original
                icon.style.transform = `scale(1) rotate(${icon.dataset.rotation}deg)`;
            }
        });
    }
}

// Scroll Reveal
function setupScrollReveal() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
}

window.addEventListener('load', () => {
    spawnIcons();
    setupMouseEffect();
    setupScrollReveal();
});

// Dark Mode Logic
const themeToggle = document.getElementById('theme-toggle');
const html = document.documentElement;

if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    html.classList.add('dark');
} else {
    html.classList.remove('dark');
}

themeToggle.addEventListener('click', () => {
    html.classList.toggle('dark');
    localStorage.theme = html.classList.contains('dark') ? 'dark' : 'light';
});
// Animação de Download (Organizar ícones)
function triggerDownloadAnimation() {
    const btn = document.getElementById('download-btn');
    const rectBtn = btn.getBoundingClientRect();
    // Centro do botão relativo ao viewport
    const btnX = rectBtn.left + rectBtn.width / 2;
    const btnY = rectBtn.top + rectBtn.height / 2;

    const wrappers = document.querySelectorAll('.icon-wrapper');

    wrappers.forEach(wrapper => {
        // 1. Congelar a posição atual
        // getBoundingClientRect retorna posições relativas ao viewport
        const rectIcon = wrapper.getBoundingClientRect();

        // Precisamos converter para absolute/fixed para a animação funcionar suavemente
        // Ou, uma vez que o wrapper é absolute relative ao container #hero,
        // podemos calcular a posição relativa ao #hero.
        // O #hero é relative, então top/left 0,0 dele é o offsetTop/offsetLeft dele na página.
        // Mas o wrapper está posicionado com % (left/top) e tem transform translate.
        // A maneira mais fácil de garantir a transição é setar estilo fixed temporariamente
        // ou calcular pixels exatos relativos ao parent. 

        // Vamos usar fixed para garantir que 'voem' por cima de tudo em direção ao botão
        wrapper.style.position = 'fixed';
        wrapper.style.left = `${rectIcon.left}px`;
        wrapper.style.top = `${rectIcon.top}px`;
        wrapper.style.margin = '0';
        wrapper.style.transform = 'none'; // Remove transforms anteriores
        wrapper.style.animation = 'none'; // Para a animação de float

        // Forçar reflow para aplicar o estilo inicial
        wrapper.offsetHeight;

        // 2. Definir transição
        wrapper.style.transition = 'all 0.8s cubic-bezier(0.55, 0.055, 0.675, 0.19)'; // Ease-in back inspired
        wrapper.style.zIndex = '100'; // Ficar por cima de tudo

        // 3. Mover para o botão
        // Pequena variação para não ficarem todos EXATAMENTE no mesmo pixel (opcional)
        wrapper.style.left = `${btnX}px`;
        wrapper.style.top = `${btnY}px`;

        // Efeito visual final
        wrapper.style.opacity = '0';
        wrapper.style.transform = 'scale(0) rotate(720deg)'; // Gira enquanto vai
    });

    // Opcional: Feedback visual no botão ou download real
    setTimeout(() => {
        // Remover ícones do DOM após animação para limpar
        wrappers.forEach(w => w.remove());

        // Aqui você iniciaria o download real se houvesse URL
        console.log("Download iniciado!");
    }, 800);
}

// Переменная для графика должна быть доступна внутри функций
let priceChart = null;

// Функция открытия модального окна (вынесена в глобальную область)
function openModal() {
    const modalOverlay = document.getElementById('modal-overlay');
    if (modalOverlay) {
        modalOverlay.style.display = 'flex';
        document.body.style.overflow = 'hidden'; // Запрещаем прокрутку страницы
        initChart(); // Запускаем отрисовку графика
    }
}

// Функция закрытия модального окна (вынесена в глобальную область)
function closeModal() {
    const modalOverlay = document.getElementById('modal-overlay');
    if (modalOverlay) {
        modalOverlay.style.display = 'none';
        document.body.style.overflow = 'auto'; // Возвращаем прокрутку страницы
    }
}

// Инициализация графика
function initChart() {
    const canvas = document.getElementById('priceChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    if (priceChart) priceChart.destroy(); // Очистка старого графика перед созданием нового

    priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['1 нед. назад', '3 дня назад', 'Сегодня'],
            datasets: [{
                label: 'Цена',
                data: [78990, 73990, 68990],
                borderColor: '#0066ff',
                backgroundColor: 'rgba(0, 102, 255, 0.1)',
                borderWidth: 3,
                pointRadius: 6,
                pointBackgroundColor: '#0066ff',
                tension: 0,
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: false, grid: { color: '#f0f0f0' } },
                x: { grid: { display: false } }
            }
        }
    });
}
function toggleFavorite() {
    const btn = document.getElementById('favBtn');
    const btnText = btn.querySelector('.btn-text');
    const heart = btn.querySelector('.heart-icon');

    // Переключаем класс active
    btn.classList.toggle('active');

    // Проверяем, есть ли класс active после переключения
    if (btn.classList.contains('active')) {
        btnText.textContent = 'В избранных';
        heart.textContent = '♥'; // Закрашенное сердце
    } else {
        btnText.textContent = 'Добавить в избранное';
        heart.textContent = '♡'; // Пустое сердце
    }
}

// Обработка событий после загрузки документа
document.addEventListener('DOMContentLoaded', () => {
    const modalOverlay = document.getElementById('modal-overlay');

    // Закрытие по клику на темный фон (оверлей)
    if (modalOverlay) {
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) {
                closeModal();
            }
        });
    }
});
// =========================
// localStorage
// =========================
function getMonitoredProducts() {
    return JSON.parse(localStorage.getItem('monitoredProducts')) || [];
}

function setMonitoredProducts(arr) {
    localStorage.setItem('monitoredProducts', JSON.stringify(arr));
}

// =========================
// Переключение кнопки
// =========================
function toggleMonitor(btn) {
    const productId = btn.dataset.productId;
    let monitored = getMonitoredProducts();

    if (monitored.includes(productId)) {
        monitored = monitored.filter(id => id !== productId);

        btn.textContent = 'Мониторить цену';
        btn.classList.remove('active');
    } else {
        monitored.push(productId);

        btn.textContent = 'Цена в отслеживании';
        btn.classList.add('active');
    }

    setMonitoredProducts(monitored);
}

// =========================
// Обновление кнопки
// =========================
function updateMonitorButton() {
    const btn = document.querySelector('.btn-monitor');
    if (!btn) return;

    const page = document.body.dataset.page;

    // 👉 ЕСЛИ МЫ НА СТРАНИЦЕ МОНИТОРИНГА
    if (page === 'monitor') {
        btn.textContent = 'Цена в отслеживании';
        btn.classList.add('active');
        return;
    }

    // 👉 ЕСЛИ МЫ НА СТРАНИЦЕ ПОИСКА
    const productId = btn.dataset.productId;
    const monitored = getMonitoredProducts();

    if (monitored.includes(productId)) {
        btn.textContent = 'Цена в отслеживании';
        btn.classList.add('active');
    } else {
        btn.textContent = 'Мониторить цену';
        btn.classList.remove('active');
    }
}

// =========================
// Клик по кнопке
// =========================
document.addEventListener('click', function (e) {
    if (e.target.classList.contains('btn-monitor')) {
        toggleMonitor(e.target);
    }
});

// =========================
// МОДАЛКА
// =========================
function openModal() {
    const modalOverlay = document.getElementById('modal-overlay');

    if (modalOverlay) {
        modalOverlay.style.display = 'flex';
        document.body.style.overflow = 'hidden';

        initChart();
        updateMonitorButton(); // 🔥 ключевой момент
    }
}

function closeModal() {
    const modalOverlay = document.getElementById('modal-overlay');

    if (modalOverlay) {
        modalOverlay.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// =========================
// Закрытие по фону
// =========================
document.addEventListener('DOMContentLoaded', () => {
    const modalOverlay = document.getElementById('modal-overlay');

    if (modalOverlay) {
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) {
                closeModal();
            }
        });
    }
});

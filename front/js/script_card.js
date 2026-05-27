// Переменная для графика должна быть доступна внутри функций
let priceChart = null;

// =========================
// РАБОТА С ИЗБРАННЫМ
// =========================
function getFavorites() {
    return JSON.parse(localStorage.getItem('favorites')) || [];
}

function setFavorites(arr) {
    localStorage.setItem('favorites', JSON.stringify(arr));
}

// Функция получения текущего товара из модального окна
function getCurrentProductFromModal() {
    const modal = document.getElementById('modal-overlay');
    if (!modal || modal.style.display !== 'flex') return null;
    
    const productName = modal.querySelector('.modal-title')?.innerText || '';
    const productPrice = modal.querySelector('.p-total')?.innerText || '';
    const productImg = modal.querySelector('.modal-product-img')?.src || '/img/product.png';
    const rating = modal.querySelector('.rating-value')?.innerText || '4.7';
    const reviewsCount = modal.querySelector('.reviews-count')?.innerText || '';
    
    if (!productName) return null;
    
    return {
        id: productName.replace(/\s/g, '_') + '_' + Date.now(),
        name: productName,
        price: productPrice,
        img: productImg,
        rating: rating,
        reviews: reviewsCount,
        addedAt: new Date().toISOString()
    };
}

// Переключение избранного
function toggleFavorite() {
    const btn = document.getElementById('favBtn');
    if (!btn) return;
    
    const btnText = btn.querySelector('.btn-text');
    const heart = btn.querySelector('.heart-icon');
    
    const product = getCurrentProductFromModal();
    if (!product || !product.name) {
        showToast('Не удалось добавить товар', 'error');
        return;
    }
    
    let favorites = getFavorites();
    // Проверяем по уникальному id или имени
    const isFavorite = favorites.some(item => item.id === product.id || item.name === product.name);
    
    if (isFavorite) {
        // Удаляем из избранного
        favorites = favorites.filter(item => item.id !== product.id && item.name !== product.name);
        btnText.textContent = 'Добавить в избранное';
        heart.textContent = '♡';
        btn.classList.remove('active');
        showToast('Товар удален из избранного', 'error');
        console.log('Товар удален из избранного:', product.name);
    } else {
        // Добавляем в избранное
        favorites.push(product);
        btnText.textContent = 'В избранных';
        heart.textContent = '♥';
        btn.classList.add('active');
        showToast('Товар добавлен в избранное!', 'success');
        console.log('Товар добавлен в избранное:', product.name);
        console.log('Всего товаров в избранном:', favorites.length);
    }
    
    setFavorites(favorites);
    updateFavoritesCount();
}

// Обновление состояния кнопки избранного при открытии модалки
function updateFavoriteButton() {
    const btn = document.getElementById('favBtn');
    if (!btn) return;
    
    const btnText = btn.querySelector('.btn-text');
    const heart = btn.querySelector('.heart-icon');
    const product = getCurrentProductFromModal();
    
    if (!product) return;
    
    const favorites = getFavorites();
    const isFavorite = favorites.some(item => item.name === product.name);
    
    if (isFavorite) {
        btnText.textContent = 'В избранных';
        heart.textContent = '♥';
        btn.classList.add('active');
    } else {
        btnText.textContent = 'Добавить в избранное';
        heart.textContent = '♡';
        btn.classList.remove('active');
    }
}

// Всплывающее уведомление
function showToast(message, type = 'success') {
    let toast = document.querySelector('.custom-toast');
    
    if (!toast) {
        toast = document.createElement('div');
        toast.className = 'custom-toast';
        document.body.appendChild(toast);
    }
    
    toast.textContent = message;
    toast.classList.add('show', type);
    
    setTimeout(() => {
        toast.classList.remove('show', type);
    }, 3000);
}

// Обновление счетчика избранного в профиле
function updateFavoritesCount() {
    const favoritesCountElement = document.getElementById('favoritesCount');
    if (favoritesCountElement) {
        const favorites = getFavorites();
        favoritesCountElement.textContent = favorites.length;
    }
}

// Функция открытия модального окна
function openModal() {
    const modalOverlay = document.getElementById('modal-overlay');
    if (modalOverlay) {
        modalOverlay.style.display = 'flex';
        document.body.style.overflow = 'hidden';
        initChart();
        updateMonitorButton();
        updateFavoriteButton();
    }
}

function closeModal() {
    const modalOverlay = document.getElementById('modal-overlay');
    if (modalOverlay) {
        modalOverlay.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

function initChart() {
    const canvas = document.getElementById('priceChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    if (priceChart) priceChart.destroy();

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

// =========================
// localStorage (мониторинг)
// =========================
function getMonitoredProducts() {
    return JSON.parse(localStorage.getItem('monitoredProducts')) || [];
}

function setMonitoredProducts(arr) {
    localStorage.setItem('monitoredProducts', JSON.stringify(arr));
}

function toggleMonitor(btn) {
    const productId = btn.dataset.productId;
    let monitored = getMonitoredProducts();

    if (monitored.includes(productId)) {
        monitored = monitored.filter(id => id !== productId);
        btn.textContent = 'Мониторить цену';
        btn.classList.remove('active');
        showToast('Товар удален из отслеживания', 'error');
    } else {
        monitored.push(productId);
        btn.textContent = 'Цена в отслеживании';
        btn.classList.add('active');
        showToast('Товар добавлен в отслеживание цены', 'success');
    }

    setMonitoredProducts(monitored);
}

function updateMonitorButton() {
    const btn = document.querySelector('.btn-monitor');
    if (!btn) return;

    const page = document.body.dataset.page;

    if (page === 'monitor') {
        btn.textContent = 'Цена в отслеживании';
        btn.classList.add('active');
        return;
    }

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

document.addEventListener('click', function (e) {
    if (e.target.classList.contains('btn-monitor')) {
        toggleMonitor(e.target);
    }
});

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

const toastStyles = document.createElement('style');
toastStyles.textContent = `
    .custom-toast {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%) translateY(100px);
        background: #333;
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        font-size: 14px;
        z-index: 10000;
        opacity: 0;
        transition: all 0.3s ease;
        pointer-events: none;
        white-space: nowrap;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .custom-toast.show {
        transform: translateX(-50%) translateY(0);
        opacity: 1;
    }
    
    .custom-toast.success {
        background: #28a745;
    }
    
    .custom-toast.error {
        background: #dc3545;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateX(-50%) translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }
    }
`;
document.head.appendChild(toastStyles);
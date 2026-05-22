// profile.js - проверка авторизации с редиректом на input.html

// Функция проверки авторизации
function checkAuthStatus() {
    return localStorage.getItem('isLoggedIn') === 'true';
}

// Функция получения текущего пользователя
function getCurrentUser() {
    return {
        username: localStorage.getItem('username') || '',
        loginTime: localStorage.getItem('loginTime') || ''
    };
}

// Ждем полной загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
    
    // Проверяем авторизацию
    const isLoggedIn = checkAuthStatus();
    
    // Если не авторизован - редирект на страницу входа
    if (!isLoggedIn) {
        window.location.href = '/input.html';
        return;
    }
    
    // Показываем блок профиля
    const profileBlock = document.getElementById('profileBlock');
    if (profileBlock) {
        profileBlock.style.display = 'block';
    }
    
    // ========== 1. РЕДАКТИРОВАНИЕ ЛИЧНОЙ ИНФОРМАЦИИ ==========
    const editBtn = document.getElementById('editInfoBtn');
    const modal = document.getElementById('editModal');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const cancelModalBtn = document.getElementById('cancelModalBtn');
    const saveModalBtn = document.getElementById('saveModalBtn');
    const editNameInput = document.getElementById('editName');
    const editEmailInput = document.getElementById('editEmail');
    const displayNameSpan = document.getElementById('displayName');
    const displayEmailSpan = document.getElementById('displayEmail');
    
    function openModal() {
        editNameInput.value = displayNameSpan.textContent;
        editEmailInput.value = displayEmailSpan.textContent;
        modal.classList.add('show');
    }
    
    function closeModal() {
        modal.classList.remove('show');
    }
    
    function saveChanges() {
        const newName = editNameInput.value.trim();
        const newEmail = editEmailInput.value.trim();
        
        if (newName === '') {
            showToast('Пожалуйста, введите имя');
            return;
        }
        
        if (newEmail === '') {
            showToast('Пожалуйста, введите email');
            return;
        }
        
        const emailPattern = /^[^\s@]+@([^\s@]+\.)+[^\s@]+$/;
        if (!emailPattern.test(newEmail)) {
            showToast('Пожалуйста, введите корректный email');
            return;
        }
        
        displayNameSpan.textContent = newName;
        displayEmailSpan.textContent = newEmail;
        saveUserDataToLocal();
        
        // Обновляем username в localStorage
        localStorage.setItem('username', newEmail);
        
        closeModal();
        showToast('Информация обновлена!');
    }
    
    function saveUserDataToLocal() {
        const existingData = localStorage.getItem('userProfile');
        let password = '';
        
        if (existingData) {
            try {
                const existingUser = JSON.parse(existingData);
                password = existingUser.password || '';
            } catch(e) {}
        }
        
        const userData = {
            name: displayNameSpan.textContent,
            email: displayEmailSpan.textContent,
            password: password,
            updatedAt: new Date().toISOString()
        };
        localStorage.setItem('userProfile', JSON.stringify(userData));
    }
    
    function loadUserDataFromLocal() {
        const savedData = localStorage.getItem('userProfile');
        if (savedData) {
            try {
                const userData = JSON.parse(savedData);
                if (userData.name) displayNameSpan.textContent = userData.name;
                if (userData.email) displayEmailSpan.textContent = userData.email;
            } catch(e) {
                console.error('Ошибка парсинга userProfile', e);
                setDefaultFromAuth();
            }
        } else {
            setDefaultFromAuth();
        }
    }
    
    function setDefaultFromAuth() {
        const username = localStorage.getItem('username');
        if (username) {
            displayEmailSpan.textContent = username;
            const nameFromEmail = username.split('@')[0];
            displayNameSpan.textContent = nameFromEmail || 'Пользователь';
            saveUserDataToLocal();
        }
    }
    
    loadUserDataFromLocal();
    
    if (editBtn) editBtn.addEventListener('click', openModal);
    if (closeModalBtn) closeModalBtn.addEventListener('click', closeModal);
    if (cancelModalBtn) cancelModalBtn.addEventListener('click', closeModal);
    if (saveModalBtn) saveModalBtn.addEventListener('click', saveChanges);
    
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeModal();
            }
        });
    }
    
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal && modal.classList.contains('show')) {
            closeModal();
        }
    });
    
    // ========== 2. ПЕРЕКЛЮЧАТЕЛЬ УВЕДОМЛЕНИЙ ==========
    const notificationToggle = document.getElementById('notificationToggle');
    const notifOffLabel = document.getElementById('notifOffLabel');
    const notifOnLabel = document.getElementById('notifOnLabel');
    
    function updateNotificationLabels(isEnabled) {
        if (isEnabled) {
            notifOffLabel.style.color = '#6c757d';
            notifOnLabel.style.color = '#28a745';
            notifOnLabel.style.fontWeight = '600';
            notifOffLabel.style.fontWeight = '400';
        } else {
            notifOffLabel.style.color = '#dc3545';
            notifOnLabel.style.color = '#6c757d';
            notifOffLabel.style.fontWeight = '600';
            notifOnLabel.style.fontWeight = '400';
        }
    }
    
    function loadNotificationState() {
        const savedState = localStorage.getItem('notificationsEnabled');
        if (savedState !== null) {
            const isEnabled = savedState === 'true';
            notificationToggle.checked = isEnabled;
            updateNotificationLabels(isEnabled);
        } else {
            notificationToggle.checked = false;
            updateNotificationLabels(false);
        }
    }
    
    function saveNotificationState(isEnabled) {
        localStorage.setItem('notificationsEnabled', isEnabled);
    }
    
    if (notificationToggle) {
        notificationToggle.addEventListener('change', function(e) {
            const isChecked = e.target.checked;
            updateNotificationLabels(isChecked);
            saveNotificationState(isChecked);
            showToast(isChecked ? 'Уведомления включены' : 'Уведомления выключены');
        });
    }
    
    loadNotificationState();
    
    // ========== 3. ПОДПИСКИ ==========
    const subCheckboxes = document.querySelectorAll('.sub-checkbox');
    
    function loadSubscriptionsState() {
        const savedSubs = localStorage.getItem('subscriptionsState');
        if (savedSubs) {
            try {
                const states = JSON.parse(savedSubs);
                subCheckboxes.forEach((checkbox, index) => {
                    if (states[index] !== undefined) {
                        checkbox.checked = states[index];
                    }
                });
            } catch(e) {}
        }
    }
    
    function saveSubscriptionsState() {
        const states = [];
        subCheckboxes.forEach(checkbox => {
            states.push(checkbox.checked);
        });
        localStorage.setItem('subscriptionsState', JSON.stringify(states));
    }
    
    loadSubscriptionsState();
    
    subCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            saveSubscriptionsState();
            const subText = this.closest('.subscription-item')?.querySelector('.sub-text')?.textContent;
            if (subText) {
                const action = this.checked ? 'подписаны на' : 'отписались от';
                showToast(`Вы ${action} «${subText}»`);
            }
        });
    });
    
    // ========== 4. КНОПКА ВЫХОДА ==========
    const logoutBtn = document.getElementById('logoutBtn');
    
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            const confirmLogout = confirm('Вы уверены, что хотите выйти из аккаунта?');
            if (confirmLogout) {
                if (typeof window.logoutUser === 'function') {
                    window.logoutUser();
                } else {
                    localStorage.removeItem('isLoggedIn');
                    localStorage.removeItem('username');
                    localStorage.removeItem('loginTime');
                    localStorage.removeItem('userProfile');
                    window.location.href = '/index.html';
                }
            }
        });
    }
    
    // ========== 5. ВКЛАДКИ (ИСПРАВЛЕНО) ==========
    const tabItems = document.querySelectorAll('.tab-item');

    // Функция для установки активной вкладки в зависимости от текущей страницы
    function setActiveTabByCurrentPage() {
        const currentPath = window.location.pathname;
        
        tabItems.forEach((tab, index) => {
            tab.classList.remove('active');
            
            // Определяем какая вкладка должна быть активной
            if (currentPath === './profile.html' || currentPath === '/' || currentPath === './index.html') {
                if (index === 0) tab.classList.add('active');
            } 
            else if (currentPath === './favourites.html') {
                if (index === 1) tab.classList.add('active');
            }
            else if (currentPath === './preferences.html') {
                if (index === 2) tab.classList.add('active');
            }
        });
    }

    // Добавляем обработчики кликов на вкладки
    tabItems.forEach((tab, index) => {
        tab.style.cursor = 'pointer';
        tab.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Переход на соответствующую страницу
            if (index === 0) {
                window.location.href = './profile.html';
            } else if (index === 1) {
                window.location.href = './favourites.html';
            } else if (index === 2) {
                window.location.href = './preferences.html';
            }
        });
    });
    
    // Устанавливаем активную вкладку при загрузке страницы
    setActiveTabByCurrentPage();
    
    // ========== 6. TOAST-УВЕДОМЛЕНИЯ ==========
    function showToast(message, duration = 2500) {
        const existingToast = document.querySelector('.custom-toast');
        if (existingToast) {
            existingToast.remove();
        }
        
        const toast = document.createElement('div');
        toast.className = 'custom-toast';
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            background: #2c3e50;
            color: white;
            padding: 10px 20px;
            border-radius: 40px;
            font-size: 14px;
            font-weight: 500;
            z-index: 2000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            animation: fadeInUp 0.3s ease;
            pointer-events: none;
        `;
        
        const style = document.querySelector('#toastAnimStyle');
        if (!style) {
            const newStyle = document.createElement('style');
            newStyle.id = 'toastAnimStyle';
            newStyle.textContent = `
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
                .custom-toast {
                    animation: fadeInUp 0.3s ease;
                }
            `;
            document.head.appendChild(newStyle);
        }
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            if (toast && toast.parentNode) {
                toast.style.opacity = '0';
                toast.style.transition = 'opacity 0.3s';
                setTimeout(() => {
                    if (toast.parentNode) toast.remove();
                }, 300);
            }
        }, duration);
    }
    
    console.log('Личный кабинет загружен (авторизован)');
});

function renderFavorites() {
    const favoritesList = document.getElementById('favorites-list');
    if (!favoritesList) return;
    
    const favorites = getFavorites();
    
    if (favorites.length === 0) {
        favoritesList.innerHTML = `
            <div class="empty-favorites">
                <p>😢 У вас пока нет избранных товаров</p>
                <a href="compare.html" class="btn-to-search">Перейти к поиску товаров</a>
            </div>
        `;
        updateFavoritesCount();
        return;
    }
    
    favoritesList.innerHTML = favorites.map((item, index) => `
        <div class="favorite-item" data-index="${index}" data-id="${item.id}">
            <img src="${item.img}" alt="${item.name}" class="favorite-img" onerror="this.src='/img/product.png'">
            <div class="favorite-info">
                <h4 class="favorite-name">${escapeHtml(item.name)}</h4>
                <div class="favorite-rating">
                    <span>⭐ ${item.rating || '4.7'}</span>
                    <span>📝 ${item.reviews || 'отзывов: 0'}</span>
                </div>
                <div class="favorite-price">${item.price || 'Цена по запросу'}</div>
                <div class="favorite-date">Добавлено: ${formatDate(item.addedAt)}</div>
            </div>
            <div class="favorite-actions">
                <button class="btn-remove-favorite" onclick="removeFavoriteItem('${item.id.replace(/'/g, "\\'")}', '${escapeHtml(item.name).replace(/'/g, "\\'")}')">🗑️ Удалить</button>
                <button class="btn-monitor-price" onclick="monitorFromFavorite('${escapeHtml(item.name).replace(/'/g, "\\'")}')">📊 Мониторить цену</button>
            </div>
        </div>
    `).join('');
    
    updateFavoritesCount();
}

// Функция для экранирования HTML
function escapeHtml(str) {
    if (!str) return '';
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

// Форматирование даты
function formatDate(dateString) {
    if (!dateString) return 'только что';
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString('ru-RU', {
            day: 'numeric',
            month: 'long',
            hour: '2-digit',
            minute: '2-digit'
        });
    } catch(e) {
        return 'недавно';
    }
}

// Удаление товара из избранного
function removeFavoriteItem(productId, productName) {
    let favorites = getFavorites();
    favorites = favorites.filter(item => item.id !== productId);
    setFavorites(favorites);
    renderFavorites();
    updateFavoritesCount();
    updateFavoriteButtonIfModalOpen();
    showToast(`Товар "${productName}" удален из избранного`, 'error');
}

// Мониторинг цены из избранного
function monitorFromFavorite(productName) {
    // Сохраняем в localStorage для отслеживания
    let monitored = getMonitoredProducts();
    if (!monitored.includes(productName)) {
        monitored.push(productName);
        setMonitoredProducts(monitored);
        showToast(`Товар "${productName}" добавлен в отслеживание цены`, 'success');
    } else {
        showToast(`Товар "${productName}" уже в отслеживании`, 'info');
    }
}

// Обновление кнопки избранного в модалке, если она открыта
function updateFavoriteButtonIfModalOpen() {
    const modal = document.getElementById('modal-overlay');
    if (modal && modal.style.display === 'flex') {
        updateFavoriteButton();
    }
}

// Переопределяем существующую функцию toggleFavorite для автоматического обновления списка
const originalToggleFavorite = toggleFavorite;
window.toggleFavorite = function() {
    originalToggleFavorite();
    // Если мы на странице избранного или профиля, обновляем список
    if (window.location.pathname.includes('favourites.html') || 
        window.location.pathname.includes('profile.html')) {
        setTimeout(renderFavorites, 100);
    }
};

// =========================
// ИНИЦИАЛИЗАЦИЯ ПРИ ЗАГРУЗКЕ
// =========================
// Сохраняем оригинальный DOMContentLoaded, добавляем свой
document.addEventListener('DOMContentLoaded', function() {
    // Если мы на странице избранного или профиля с активной вкладкой избранного
    if (window.location.pathname.includes('favourites.html')) {
        renderFavorites();
    }
    
    // Для страницы profile.html - отслеживаем переключение вкладок
    const favTab = document.querySelector('.tab-item:nth-child(2)');
    if (favTab) {
        const originalClick = favTab.onclick;
        favTab.addEventListener('click', function() {
            setTimeout(renderFavorites, 50);
        });
    }
});
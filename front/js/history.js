// Ключ для хранения истории поиска в localStorage
const SEARCH_HISTORY_KEY = 'vzglyad_search_history';

// Функция для проверки авторизации
function isLoggedIn() {
    return localStorage.getItem('isLoggedIn') === 'true';
}

// Функция для получения ключа истории с учётом пользователя
function getSearchHistoryKey() {
    const username = localStorage.getItem('username');
    if (username) {
        return `vzglyad_search_history_${username}`;
    }
    return SEARCH_HISTORY_KEY;
}

// Функция для получения истории из localStorage
function getSearchHistory() {
    // Если пользователь не авторизован - возвращаем пустую историю
    if (!isLoggedIn()) {
        return [];
    }
    
    const historyKey = getSearchHistoryKey();
    const history = localStorage.getItem(historyKey);
    if (!history) {
        return [];
    }
    try {
        return JSON.parse(history);
    } catch (e) {
        console.error('Ошибка при парсинге истории:', e);
        return [];
    }
}

// Функция для сохранения истории в localStorage
function saveSearchHistory(history) {
    if (!isLoggedIn()) return;
    
    const historyKey = getSearchHistoryKey();
    localStorage.setItem(historyKey, JSON.stringify(history));
}

// Функция для удаления конкретной записи из истории
function removeFromHistory(id) {
    let history = getSearchHistory();
    history = history.filter(item => item.id !== id);
    saveSearchHistory(history);
    renderHistory();
}

// Функция для очистки всей истории
function clearAllHistory() {
    if (confirm('Вы уверены, что хотите очистить всю историю поиска?')) {
        saveSearchHistory([]);
        renderHistory();
    }
}

// Функция для повторного поиска по запросу
function repeatSearch(query) {
    // Сохраняем запрос в историю только если авторизован
    if (isLoggedIn()) {
        addToSearchHistory(query);
    }
    // Перенаправляем на главную страницу с параметром поиска
    window.location.href = `/index.html?search=${encodeURIComponent(query)}`;
}

// Функция для добавления в историю (только для авторизованных)
function addToSearchHistory(query) {
    if (!isLoggedIn()) return;
    if (!query || query.trim() === '') return;
    
    const history = getSearchHistory();
    const now = new Date();
    
    const newEntry = {
        id: Date.now(),
        query: query.trim(),
        timestamp: now.toISOString(),
        formattedDate: formatDate(now)
    };
    
    // Удаляем дубликаты
    const filteredHistory = history.filter(item => item.query.toLowerCase() !== query.trim().toLowerCase());
    
    filteredHistory.unshift(newEntry);
    const limitedHistory = filteredHistory.slice(0, 50);
    
    saveSearchHistory(limitedHistory);
}

// Функция форматирования даты
function formatDate(date) {
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    return `${day}.${month}.${year} ${hours}:${minutes}:${seconds}`;
}

// Функция для получения относительного времени (сколько времени назад)
function getRelativeTime(timestamp) {
    const now = new Date();
    const past = new Date(timestamp);
    const diffMs = now - past;
    const diffSeconds = Math.floor(diffMs / 1000);
    const diffMinutes = Math.floor(diffSeconds / 60);
    const diffHours = Math.floor(diffMinutes / 60);
    const diffDays = Math.floor(diffHours / 24);
    const diffWeeks = Math.floor(diffDays / 7);
    const diffMonths = Math.floor(diffDays / 30);
    const diffYears = Math.floor(diffDays / 365);
    
    if (diffSeconds < 5) {
        return 'только что';
    } else if (diffSeconds < 60) {
        return `${diffSeconds} секунд назад`;
    } else if (diffMinutes < 60) {
        const minutes = diffMinutes;
        const lastDigit = minutes % 10;
        const lastTwoDigits = minutes % 100;
        
        if (lastTwoDigits >= 11 && lastTwoDigits <= 14) {
            return `${minutes} минут назад`;
        }
        if (lastDigit === 1) return `${minutes} минуту назад`;
        if (lastDigit >= 2 && lastDigit <= 4) return `${minutes} минуты назад`;
        return `${minutes} минут назад`;
    } else if (diffHours < 24) {
        const hours = diffHours;
        const lastDigit = hours % 10;
        const lastTwoDigits = hours % 100;
        
        if (lastTwoDigits >= 11 && lastTwoDigits <= 14) {
            return `${hours} часов назад`;
        }
        if (lastDigit === 1) return `${hours} час назад`;
        if (lastDigit >= 2 && lastDigit <= 4) return `${hours} часа назад`;
        return `${hours} часов назад`;
    } else if (diffDays < 7) {
        const days = diffDays;
        const lastDigit = days % 10;
        const lastTwoDigits = days % 100;
        
        if (lastTwoDigits >= 11 && lastTwoDigits <= 14) {
            return `${days} дней назад`;
        }
        if (lastDigit === 1) return `${days} день назад`;
        if (lastDigit >= 2 && lastDigit <= 4) return `${days} дня назад`;
        return `${days} дней назад`;
    } else if (diffWeeks < 4) {
        const weeks = diffWeeks;
        const lastDigit = weeks % 10;
        
        if (lastDigit === 1) return `${weeks} неделю назад`;
        if (lastDigit >= 2 && lastDigit <= 4) return `${weeks} недели назад`;
        return `${weeks} недель назад`;
    } else if (diffMonths < 12) {
        const months = diffMonths;
        const lastDigit = months % 10;
        const lastTwoDigits = months % 100;
        
        if (lastTwoDigits >= 11 && lastTwoDigits <= 14) {
            return `${months} месяцев назад`;
        }
        if (lastDigit === 1) return `${months} месяц назад`;
        if (lastDigit >= 2 && lastDigit <= 4) return `${months} месяца назад`;
        return `${months} месяцев назад`;
    } else {
        const years = diffYears;
        const lastDigit = years % 10;
        const lastTwoDigits = years % 100;
        
        if (lastTwoDigits >= 11 && lastTwoDigits <= 14) {
            return `${years} лет назад`;
        }
        if (lastDigit === 1) return `${years} год назад`;
        if (lastDigit >= 2 && lastDigit <= 4) return `${years} года назад`;
        return `${years} лет назад`;
    }
}

// Функция для отображения истории на странице
function renderHistory() {
    const historyList = document.getElementById('historyList');
    if (!historyList) return;
    
    const history = getSearchHistory();
    
    if (!isLoggedIn()) {
        historyList.innerHTML = `
            <div class="empty-history">
                <p>🔒 История поиска доступна только авторизованным пользователям</p>
                <p style="font-size: 20px; margin-top: 8px;">
                    <a href="/input.html" style="color: #007bff;">Войдите в аккаунт</a>, чтобы просматривать историю
                </p>
            </div>
        `;
        return;
    }
    
    if (history.length === 0) {
        historyList.innerHTML = `
            <div class="empty-history">
                <p>📭 История поиска пуста</p>
                <p style="font-size: 20px; margin-top: 8px;">Начните искать товары на главной странице</p>
            </div>
        `;
        return;
    }
    
    historyList.innerHTML = history.map(item => {
        const relativeTime = getRelativeTime(item.timestamp);
        return `
            <div class="history-item" data-id="${item.id}">
                <div class="history-query">
                    <img src="/img/input-black.png">
                    <span class="query-text">${escapeHtml(item.query)}</span>
                </div>
                <div class="history-info">
                    <span class="history-time">${relativeTime}</span>
                    <div class="history-actions">
                        <button class="repeat-search-btn" data-query="${escapeHtml(item.query)}">Сравнить товары</button>
                        <button class="delete-item-btn" data-id="${item.id}"><img src="/img/delete.png"></button>
                    </div>
                </div>
            </div>
        `;
    }).join('');
    
    // Добавляем обработчики для кнопок удаления
    document.querySelectorAll('.delete-item-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const id = parseInt(btn.dataset.id);
            removeFromHistory(id);
        });
    });
    
    // Добавляем обработчики для кнопок повторного поиска
    document.querySelectorAll('.repeat-search-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const query = btn.dataset.query;
            repeatSearch(query);
        });
    });
}

// Функция для экранирования HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Инициализация страницы истории
if (document.getElementById('historyList')) {
    document.addEventListener('DOMContentLoaded', () => {
        renderHistory();
        
        const clearBtn = document.getElementById('clearHistoryBtn');
        if (clearBtn) {
            clearBtn.addEventListener('click', clearAllHistory);
        }
        
        // Слушаем изменения в localStorage из других вкладок
        window.addEventListener('storage', (e) => {
            const username = localStorage.getItem('username');
            if (e.key === `vzglyad_search_history_${username}` || e.key === 'isLoggedIn') {
                renderHistory();
            }
        });
    });
}
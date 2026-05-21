const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const chips = document.querySelectorAll('.chip');

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

function getSearchHistory() {
    // Если пользователь не авторизован - возвращаем пустую историю
    if (!isLoggedIn()) {
        return [];
    }
    
    const historyKey = getSearchHistoryKey();
    const history = localStorage.getItem(historyKey);
    if (!history) return [];
    try {
        return JSON.parse(history);
    } catch (e) {
        console.error('Ошибка при парсинге истории:', e);
        return [];
    }
}

function saveSearchHistory(history) {
    // Сохраняем только если пользователь авторизован
    if (!isLoggedIn()) {
        return;
    }
    
    const historyKey = getSearchHistoryKey();
    localStorage.setItem(historyKey, JSON.stringify(history));
}

function formatDate(date) {
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    return `${day}.${month}.${year} ${hours}:${minutes}:${seconds}`;
}

function addToSearchHistory(query) {
    // Сохраняем ТОЛЬКО если пользователь авторизован
    if (!isLoggedIn()) {
        console.log('Неавторизованный пользователь - история не сохраняется');
        return;
    }
    
    if (!query || query.trim() === '') return;
    
    const history = getSearchHistory();
    const now = new Date();
    
    const newEntry = {
        id: Date.now(),
        query: query.trim(),
        timestamp: now.toISOString(),
        formattedDate: formatDate(now)
    };
    
    const filteredHistory = history.filter(item => item.query.toLowerCase() !== query.trim().toLowerCase());
    filteredHistory.unshift(newEntry);
    const limitedHistory = filteredHistory.slice(0, 50);
    
    saveSearchHistory(limitedHistory);
    
    window.dispatchEvent(new StorageEvent('storage', {
        key: getSearchHistoryKey(),
        newValue: JSON.stringify(limitedHistory)
    }));
}

function performSearch() {
    const query = searchInput.value.trim();
    if (query) {
        // Сохраняем в историю ТОЛЬКО если авторизован
        if (isLoggedIn()) {
            addToSearchHistory(query);
        } else {
            console.log('Поиск выполнен неавторизованным пользователем, история не сохранена');
        }
        
        console.log('Поиск:', query);
        // Здесь можно добавить реальную логику поиска
        // alert('Поиск: ' + query); // убираем alert
        
        // Раскомментируйте для перехода на страницу результатов:
        // window.location.href = '/search-results.html?q=' + encodeURIComponent(query);
    } else if (query === '') {
        searchInput.style.border = '2px solid #ff4444';
        searchInput.placeholder = 'Введите запрос для поиска';
        setTimeout(() => {
            searchInput.style.border = '';
            searchInput.placeholder = 'iPhone 15 128GB черный';
        }, 2000);
        searchInput.focus();
    }
}

function setSearchQuery(query) {
    searchInput.value = query;
    searchInput.focus();
}

searchInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        performSearch();
    }
});

searchBtn.addEventListener('click', performSearch);

chips.forEach(chip => {
    chip.addEventListener('click', () => {
        const query = chip.getAttribute('data-query');
        if (query) {
            setSearchQuery(query);
            performSearch();
        }
    });
});

// При изменении статуса авторизации
window.addEventListener('storage', function(event) {
    if (event.key === 'isLoggedIn') {
        console.log('Статус авторизации изменился');
    }
});
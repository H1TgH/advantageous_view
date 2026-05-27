// preferences.js - управление приоритетами (без ограничений на уникальность)
(function() {
    // Состояние предпочтений
    let preferences = {
        price: null,      // 1, 2 или 3
        speed: null,
        reliability: null
    };

    // DOM элементы
    const cards = {
        price: document.querySelector('[data-criterion="price"]'),
        speed: document.querySelector('[data-criterion="speed"]'),
        reliability: document.querySelector('[data-criterion="reliability"]')
    };
    
    const saveBtn = document.getElementById('savePreferencesBtn');
    const resetBtn = document.getElementById('resetPreferencesBtn');
    const messageDiv = document.getElementById('preferencesMessage');
    
    // Вспомогательная функция для отображения сообщений
    function showMessage(text, type = 'success') {
        if (!messageDiv) return;
        messageDiv.textContent = text;
        messageDiv.className = `message-area ${type}`;
        setTimeout(() => {
            if (messageDiv) {
                messageDiv.className = 'message-area';
                messageDiv.textContent = '';
            }
        }, 3000);
    }
    
    // Обновить UI кнопок (активные состояния)
    function updateButtonsUI() {
        for (const [criterion, currentValue] of Object.entries(preferences)) {
            const container = document.querySelector(`.priority-buttons[data-criterion="${criterion}"]`);
            if (!container) continue;
            
            const buttons = container.querySelectorAll('.priority-btn');
            buttons.forEach(btn => {
                const btnValue = parseInt(btn.dataset.value);
                btn.classList.remove('active');
                
                if (currentValue === btnValue) {
                    btn.classList.add('active');
                }
            });
            
            
        }
    }
    
    // Установить приоритет для критерия
    function setPriority(criterion, value) {
        // Просто сохраняем значение без проверок уникальности
        preferences[criterion] = value;
        
        // Обновляем интерфейс
        updateButtonsUI();
        return true;
    }
    
    // Сброс всех предпочтений
    function resetPreferences() {
        preferences = {
            price: null,
            speed: null,
            reliability: null
        };
        updateButtonsUI();
        showMessage('Все предпочтения сброшены', 'success');
    }
    
    // Сохранение предпочтений (в localStorage)
    function savePreferences() {
        // Проверяем, что все три критерия имеют выбранные значения
        const allSelected = Object.values(preferences).every(v => v !== null);
        if (!allSelected) {
            showMessage('⚠️ Пожалуйста, назначьте приоритеты для всех трёх критериев (Цена, Скорость, Надежность).', 'error');
            return false;
        }
        
        // Сохраняем в localStorage
        localStorage.setItem('userPreferences', JSON.stringify(preferences));
        
        // Выводим информацию о сохранённых предпочтениях
        const prefText = `Цена: ${preferences.price}, Скорость: ${preferences.speed}, Надежность: ${preferences.reliability}`;
        showMessage(`✅ Предпочтения успешно сохранены! ${prefText}`, 'success');
        
        // Генерируем событие для других модулей
        const event = new CustomEvent('preferencesSaved', { detail: preferences });
        document.dispatchEvent(event);
        
        console.log('Сохранённые предпочтения:', preferences);
        return true;
    }
    
    // Загрузить сохранённые предпочтения из localStorage
    function loadSavedPreferences() {
        const saved = localStorage.getItem('userPreferences');
        if (saved) {
            try {
                const parsed = JSON.parse(saved);
                if (parsed.hasOwnProperty('price') && parsed.hasOwnProperty('speed') && parsed.hasOwnProperty('reliability')) {
                    preferences = parsed;
                    updateButtonsUI();
                }
            } catch(e) { 
                console.warn('Ошибка загрузки предпочтений'); 
            }
        }
    }
    
    // Обработчики кликов по кнопкам приоритетов
    function bindEvents() {
        document.querySelectorAll('.priority-btn').forEach(btn => {
            btn.removeEventListener('click', priorityClickHandler);
            btn.addEventListener('click', priorityClickHandler);
        });
        
        if (saveBtn) saveBtn.addEventListener('click', savePreferences);
        if (resetBtn) resetBtn.addEventListener('click', resetPreferences);
    }
    
    function priorityClickHandler(event) {
        const btn = event.currentTarget;
        const value = parseInt(btn.dataset.value);
        const container = btn.closest('.priority-buttons');
        if (!container) return;
        const criterion = container.dataset.criterion;
        if (criterion && ['price', 'speed', 'reliability'].includes(criterion)) {
            setPriority(criterion, value);
        }
    }
    
    // Инициализация
    function init() {
        loadSavedPreferences();
        bindEvents();
        updateButtonsUI();
        console.log('Страница предпочтений загружена (уникальность отключена)');
    }
    
    // Запускаем после полной загрузки DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
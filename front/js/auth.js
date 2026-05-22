// Функция для обновления кнопки на "Войти"
function updateButtonToLogin(buttonElement) {
    buttonElement.innerHTML = '<img src="./img/input.png" style="height: 40px; width: 40px;">Войти ';
    buttonElement.setAttribute('data-status', 'logged-out');
    buttonElement.title = "Войти в аккаунт";
}

// Функция для обновления кнопки на "Профиль"
function updateButtonToProfile(buttonElement) {
    buttonElement.innerHTML = '<img src="./img/white-search.png" style="height: 40px; width: 40px;"> Личный кабинет';
    buttonElement.setAttribute('data-status', 'logged-in');
    buttonElement.title = "Перейти в профиль";
}

// Проверяем статус авторизации
function checkAuthStatus() {
    return localStorage.getItem('isLoggedIn') === 'true';
}

// Получаем имя пользователя
function getUsername() {
    return localStorage.getItem('username') || 'Пользователь';
}

// Функция для обновления видимости элементов навигации и CTA блока
function updateVisibilityByAuthStatus() {
    const isLoggedIn = checkAuthStatus();
    
    // Элементы навигации, которые показываются только авторизованным пользователям
    const navCompare = document.getElementById('compar');
    const navTrack = document.getElementById('track');
    const navHistory = document.getElementById('history');
    
    // CTA блок (призыв зарегистрироваться/войти)
    const ctaSection = document.getElementById('ctasection');
    
    if (isLoggedIn) {
        // Пользователь авторизован - показываем дополнительные пункты меню
        if (navCompare) navCompare.style.display = 'list-item';
        if (navTrack) navTrack.style.display = 'list-item';
        if (navHistory) navHistory.style.display = 'list-item';
        
        // Скрываем CTA блок
        if (ctaSection) ctaSection.style.display = 'none';
    } else {
        // Пользователь не авторизован - скрываем дополнительные пункты меню
        if (navCompare) navCompare.style.display = 'none';
        if (navTrack) navTrack.style.display = 'none';
        if (navHistory) navHistory.style.display = 'none';
        
        // Показываем CTA блок
        if (ctaSection) ctaSection.style.display = 'block';
    }
}

// Инициализация кнопки авторизации
function initAuthButton() {
    const userAuthButton = document.getElementById('userAuthButton');
    
    if (!userAuthButton) {
        console.log('Кнопка авторизации не найдена');
        return;
    }
    
    const isLoggedIn = checkAuthStatus();
    
    if (isLoggedIn) {
        updateButtonToProfile(userAuthButton);
    } else {
        updateButtonToLogin(userAuthButton);
    }
    
    // Добавляем обработчик клика на кнопку
    userAuthButton.addEventListener('click', function() {
        const status = userAuthButton.getAttribute('data-status');
        
        if (status === 'logged-in') {
            // Если авторизован - переход в профиль
            window.location.href = './profile.html';
        } else {
            // Если не авторизован - переход на страницу входа
            window.location.href = './input.html';
        }
    });
    
    // Обновляем видимость элементов при инициализации
    updateVisibilityByAuthStatus();
}

// Вход пользователя
function loginUser(login, password) {
    
    if (login && password) {
        // Сохраняем статус входа в localStorage
        localStorage.setItem('isLoggedIn', 'true');
        localStorage.setItem('username', login);
        localStorage.setItem('loginTime', new Date().toISOString());
        
        // === ДОБАВЛЯЕМ СОХРАНЕНИЕ ПРОФИЛЯ ===
        const userProfile = {
            name: login.split('@')[0] || 'Пользователь',  // берём имя из почты
            email: login,
            password: password,
            createdAt: new Date().toISOString()
        };
        localStorage.setItem('userProfile', JSON.stringify(userProfile));
        // ====================================
        
        // Обновляем видимость элементов после входа
        updateVisibilityByAuthStatus();
        
        // Обновляем кнопку
        const userAuthButton = document.getElementById('userAuthButton');
        if (userAuthButton) {
            updateButtonToProfile(userAuthButton);
        }
        
        return { success: true, username: login };
    } else {
        return { success: false, message: 'Заполните все поля' };
    }
}

// Выход пользователя
function logoutUser() {
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('username');
    localStorage.removeItem('loginTime');
    
    // Обновляем видимость элементов после выхода
    updateVisibilityByAuthStatus();
    
    // Перенаправляем на главную страницу
    window.location.href = './index.html';
}

// Проверка доступа к защищенным страницам
function requireAuth(redirectTo = './input.html') {
    if (!checkAuthStatus()) {
        window.location.href = redirectTo;
        return false;
    }
    return true;
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('userAuthButton')) {
        initAuthButton();
    }
    
    // Слушаем изменения localStorage для синхронизации между вкладками
    window.addEventListener('storage', function(event) {
        if (event.key === 'isLoggedIn') {
            updateVisibilityByAuthStatus();
            
            // Обновляем кнопку
            const userAuthButton = document.getElementById('userAuthButton');
            if (userAuthButton) {
                if (checkAuthStatus()) {
                    updateButtonToProfile(userAuthButton);
                } else {
                    updateButtonToLogin(userAuthButton);
                }
            }
        }
    });
});
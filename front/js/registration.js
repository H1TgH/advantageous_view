// register.js - обработка регистрации

document.addEventListener('DOMContentLoaded', function() {
    const registerBtn = document.getElementById('registerBtn');
    
    if (!registerBtn) return;
    
    registerBtn.addEventListener('click', function(e) {
        // Получаем значения полей
        const name = document.getElementById('lastName').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        const consent = document.getElementById('consentCheckbox').checked;

        // Валидация
        if (!name) {
            alert('Введите имя');
            return;
        }

        if (!email) {
            alert('Введите email');
            return;
        }

        // Проверка формата email
        const emailPattern = /^[^\s@]+@([^\s@]+\.)+[^\s@]+$/;
        if (!emailPattern.test(email)) {
            alert('Введите корректный email');
            return;
        }

        if (!password) {
            alert('Введите пароль');
            return;
        }

        if (password.length < 6) {
            alert('Пароль должен содержать минимум 6 символов');
            return;
        }

        if (password !== confirmPassword) {
            alert('Пароли не совпадают');
            return;
        }

        if (!consent) {
            alert('Подтвердите согласие на обработку персональных данных');
            return;
        }

        // Проверка на существующего пользователя
        const existingProfile = localStorage.getItem('userProfile');
        if (existingProfile) {
            try {
                const existingUser = JSON.parse(existingProfile);
                if (existingUser.email === email) {
                    alert('Пользователь с таким email уже зарегистрирован');
                    return;
                }
            } catch(e) {
                console.error('Ошибка парсинга существующего профиля', e);
            }
        }

        // Сохраняем данные пользователя
        const userData = {
            name: name,
            email: email,
            password: password,
            registeredAt: new Date().toISOString()
        };

        localStorage.setItem('userProfile', JSON.stringify(userData));
        
        // Устанавливаем статус авторизации
        localStorage.setItem('isLoggedIn', 'true');
        localStorage.setItem('username', email);
        localStorage.setItem('loginTime', new Date().toISOString());

        // Показываем сообщение и переходим в профиль
        alert('Регистрация прошла успешно!');
        window.location.href = '/profile.html';
    });
});
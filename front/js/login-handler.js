// js/login-handler.js

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('.registration-form');
    
    if (!loginForm) return;
    
    const loginInput = document.getElementById('login');
    const passwordInput = document.getElementById('password');
    
    loginForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        const email = loginInput?.value.trim();
        const password = passwordInput?.value;
        
        if (!email || !password) {
            showMessage('Заполните все поля', 'error');
            return;
        }
        
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(email)) {
            showMessage('Введите корректный email', 'error');
            return;
        }
        
        const submitBtn = loginForm.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.textContent = 'Вход...';
        }
        
        try {
            const response = await fetch('http://localhost:8000/api/v1/users/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });
            
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.detail || 'Неверный логин или пароль');
            }
            
            if (result.access_token && result.refresh_token) {
                // Сохраняем токены
                localStorage.setItem('access_token', result.access_token);
                localStorage.setItem('refresh_token', result.refresh_token);
                localStorage.setItem('isLoggedIn', 'true');
                localStorage.setItem('username', email);
                localStorage.setItem('loginTime', new Date().toISOString());
                
                // ВАЖНО: Проверяем, есть ли сохраненный профиль с именем
                const existingProfile = JSON.parse(localStorage.getItem('userProfile') || '{}');
                
                // Если уже есть userProfile с именем - сохраняем его
                // Если нет - создаем новый с email
                if (existingProfile.name && existingProfile.name.trim() !== '') {
                    // Имя уже есть в профиле - используем его
                    localStorage.setItem('userProfile', JSON.stringify({
                        name: existingProfile.name,
                        email: email,
                        password: password
                    }));
                } else {
                    // Имени нет - берем из email (часть до @)
                    localStorage.setItem('userProfile', JSON.stringify({
                        name: email.split('@')[0],  //zuhroyakub из zuhroyakub@gmail.com
                        email: email,
                        password: password
                    }));
                }
                
                showMessage('✅ Вход выполнен успешно!', 'success');
                
                // Обновляем UI
                if (typeof updateAuthButton === 'function') updateAuthButton();
                if (typeof updateVisibilityByAuthStatus === 'function') updateVisibilityByAuthStatus();
                
                setTimeout(() => {
                    window.location.href = './index.html';
                }, 1000);
            }
            
        } catch (error) {
            console.error('Login error:', error);
            showMessage('❌ ' + error.message, 'error');
        } finally {
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Войти';
            }
        }
    });
    
    function showMessage(text, type) {
        const old = document.querySelector('.login-message');
        if (old) old.remove();
        
        const msg = document.createElement('div');
        msg.className = `login-message ${type}`;
        msg.textContent = text;
        msg.style.cssText = `
            padding: 12px 16px;
            margin: 10px 0;
            border-radius: 8px;
            text-align: center;
            font-weight: 500;
            ${type === 'error' 
                ? 'background: #ffebee; color: #c62828; border: 1px solid #ef9a9a;' 
                : 'background: #e8f5e9; color: #2e7d32; border: 1px solid #a5d6a7;'
            }
        `;
        
        loginForm.insertBefore(msg, loginForm.firstChild);
        
        setTimeout(() => {
            msg.style.transition = 'opacity 0.3s';
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 300);
        }, type === 'success' ? 1000 : 5000);
    }
});
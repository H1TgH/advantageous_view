// js/registration.js

document.addEventListener('DOMContentLoaded', function() {
    const registerBtn = document.getElementById('registerBtn');
    
    if (!registerBtn) return;
    
    const fields = {
        name: document.getElementById('lastName'),
        email: document.getElementById('email'),
        password: document.getElementById('password'),
        confirmPassword: document.getElementById('confirmPassword'),
        consent: document.getElementById('consentCheckbox')
    };
    
    function showError(input, message) {
        input.style.borderColor = '#c62828';
        const group = input.closest('.input-group');
        let error = group.querySelector('.error-message');
        if (!error) {
            error = document.createElement('small');
            error.className = 'error-message';
            error.style.color = '#c62828';
            error.style.fontSize = '12px';
            error.style.marginTop = '5px';
            error.style.display = 'block';
            group.appendChild(error);
        }
        error.textContent = message;
    }
    
    function clearError(input) {
        input.style.borderColor = '';
        const group = input.closest('.input-group');
        const error = group?.querySelector('.error-message');
        if (error) error.remove();
    }
    
    function validateName() {
        const value = fields.name.value.trim();
        if (value.length < 2) {
            showError(fields.name, 'Имя должно содержать минимум 2 символа');
            return false;
        }
        clearError(fields.name);
        return true;
    }
    
    function validateEmail() {
        const value = fields.email.value.trim();
        const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!pattern.test(value)) {
            showError(fields.email, 'Введите корректный email');
            return false;
        }
        clearError(fields.email);
        return true;
    }
    
    function validatePassword() {
        const value = fields.password.value;
        if (value.length < 6) {
            showError(fields.password, 'Пароль должен содержать минимум 6 символов');
            return false;
        }
        clearError(fields.password);
        return true;
    }
    
    function validateConfirmPassword() {
        if (fields.password.value !== fields.confirmPassword.value) {
            showError(fields.confirmPassword, 'Пароли не совпадают');
            return false;
        }
        clearError(fields.confirmPassword);
        return true;
    }
    
    function validateConsent() {
        if (!fields.consent.checked) {
            showError(fields.consent, 'Необходимо принять соглашение');
            return false;
        }
        clearError(fields.consent);
        return true;
    }
    
    fields.name?.addEventListener('blur', validateName);
    fields.email?.addEventListener('blur', validateEmail);
    fields.password?.addEventListener('blur', validatePassword);
    fields.confirmPassword?.addEventListener('blur', validateConfirmPassword);
    fields.consent?.addEventListener('change', validateConsent);
    
    registerBtn.addEventListener('click', async function(e) {
        e.preventDefault();
        
        const isValid = validateName() && validateEmail() && validatePassword() && 
                       validateConfirmPassword() && validateConsent();
        
        if (!isValid) {
            alert('Исправьте ошибки в форме');
            return;
        }
        
        registerBtn.disabled = true;
        registerBtn.textContent = 'Регистрация...';
        
        try {
            const registrationData = {
                name: fields.name.value.trim(),      // ИМЯ
                email: fields.email.value.trim(),    // EMAIL
                password: fields.password.value      // ПАРОЛЬ
            };
            
            // Отправка на бэкенд
            const response = await fetch('http://localhost:8000/api/v1/users/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(registrationData)
            });
            
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.detail || 'Ошибка регистрации');
            }
            
            alert('✅ Регистрация прошла успешно!');
            
            // Автоматический вход
            const loginResponse = await fetch('http://localhost:8000/api/v1/users/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: registrationData.email,
                    password: registrationData.password
                })
            });
            
            const loginResult = await loginResponse.json();
            
            if (loginResponse.ok && loginResult.access_token) {
                // Сохраняем токены
                localStorage.setItem('access_token', loginResult.access_token);
                localStorage.setItem('refresh_token', loginResult.refresh_token);
                localStorage.setItem('isLoggedIn', 'true');
                localStorage.setItem('username', registrationData.email);
                localStorage.setItem('loginTime', new Date().toISOString());
                
                // ВАЖНО: Сохраняем ИМЯ и EMAIL раздельно
                localStorage.setItem('userProfile', JSON.stringify({
                    name: registrationData.name,      // ← ИМЯ (zuhroyakub)
                    email: registrationData.email,    // ← EMAIL (zuhroyakub@gmail.com)
                    password: registrationData.password
                }));
                
                // Обновляем UI
                if (typeof updateAuthButton === 'function') updateAuthButton();
                if (typeof updateVisibilityByAuthStatus === 'function') updateVisibilityByAuthStatus();
                
                window.location.href = './profile.html';
            }
            
        } catch (error) {
            console.error('Registration error:', error);
            alert('❌ ' + error.message);
        } finally {
            registerBtn.disabled = false;
            registerBtn.textContent = 'Далее';
        }
    });
});
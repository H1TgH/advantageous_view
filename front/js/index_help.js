// Валидация формы регистрации
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.registration-form');
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirmPassword');
    const emailInput = document.getElementById('email');
    const lastNameInput = document.getElementById('lastName');
    const consentCheckbox = document.getElementById('consentCheckbox');
    const nextButton = document.querySelector('.cta-button');
    
    // Функция проверки совпадения паролей
    function checkPasswordsMatch() {
        if (password.value !== confirmPassword.value) {
            confirmPassword.setCustomValidity('Пароли не совпадают');
            return false;
        } else {
            confirmPassword.setCustomValidity('');
            return true;
        }
    }
    
    // Функция проверки длины пароля
    function checkPasswordStrength() {
        if (password.value.length > 0 && password.value.length < 6) {
            password.setCustomValidity('Пароль должен содержать не менее 6 символов');
            return false;
        } else {
            password.setCustomValidity('');
            return true;
        }
    }
    
    // Функция проверки email
    function checkEmail() {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (emailInput.value.length > 0 && !emailPattern.test(emailInput.value)) {
            emailInput.setCustomValidity('Введите корректный email (пример: name@domain.ru)');
            return false;
        } else {
            emailInput.setCustomValidity('');
            return true;
        }
    }
    
    // Функция проверки имени
    function checkName() {
        if (lastNameInput.value.length > 0 && lastNameInput.value.length < 2) {
            lastNameInput.setCustomValidity('Имя должно содержать не менее 2 символов');
            return false;
        } else {
            lastNameInput.setCustomValidity('');
            return true;
        }
    }
    
    // Функция проверки согласия на обработку данных
    function checkConsent() {
        if (!consentCheckbox || !consentCheckbox.checked) {
            if (consentCheckbox) {
                consentCheckbox.setCustomValidity('Необходимо принять условия соглашения');
            }
            return false;
        } else {
            if (consentCheckbox) {
                consentCheckbox.setCustomValidity('');
            }
            return true;
        }
    }
    
    // Добавляем обработчики событий
    if (password && confirmPassword) {
        password.addEventListener('input', function() {
            checkPasswordStrength();
            if (confirmPassword.value.length > 0) {
                checkPasswordsMatch();
            }
        });
        
        confirmPassword.addEventListener('input', checkPasswordsMatch);
    }
    
    if (emailInput) {
        emailInput.addEventListener('input', checkEmail);
    }
    
    if (lastNameInput) {
        lastNameInput.addEventListener('input', checkName);
    }
    
    if (consentCheckbox) {
        consentCheckbox.addEventListener('change', checkConsent);
    }
    
    // Обработка отправки формы
    if (form) {
        form.addEventListener('submit', function(event) {
            const isNameValid = checkName();
            const isEmailValid = checkEmail();
            const isPasswordStrong = checkPasswordStrength();
            const isPasswordsMatch = checkPasswordsMatch();
            const isConsentGiven = checkConsent();
            
            if (!isNameValid || !isEmailValid || !isPasswordStrong || !isPasswordsMatch || !isConsentGiven) {
                event.preventDefault();
                alert('' +
                      (!isNameValid ? '- Имя должно содержать не менее 2 символов\n' : '') +
                      (!isEmailValid ? '- Введите корректный email\n' : '') +
                      (!isPasswordStrong ? '- Пароль должен содержать не менее 6 символов\n' : '') +
                      (!isPasswordsMatch ? '- Пароли не совпадают\n' : '') +
                      (!isConsentGiven ? '- Необходимо принять условия соглашения и дать согласие на обработку персональных данных\n' : ''));
            }
        });
    }
    
    // Обработка кнопки "Далее" (если это переход без отправки формы)
    if (nextButton) {
        nextButton.addEventListener('click', function(event) {
            const isNameValid = checkName();
            const isEmailValid = checkEmail();
            const isPasswordStrong = checkPasswordStrength();
            const isPasswordsMatch = checkPasswordsMatch();
            const isConsentGiven = checkConsent();
            
            // Проверка на заполненность полей
            const isNameFilled = lastNameInput.value.trim() !== '';
            const isEmailFilled = emailInput.value.trim() !== '';
            const isPasswordFilled = password.value !== '';
            const isConfirmFilled = confirmPassword.value !== '';
            const allFieldsFilled = isNameFilled && isEmailFilled && isPasswordFilled && isConfirmFilled;
            
            // Сбор ошибок для детального сообщения
            const errors = [];
            
            if (!allFieldsFilled) {
                errors.push('Заполните все поля');
            }
            if (!isNameValid) {
                errors.push('Имя должно содержать не менее 2 символов');
            }
            if (!isEmailValid) {
                errors.push('Введите корректный email');
            }
            if (!isPasswordStrong) {
                errors.push('Пароль должен содержать не менее 6 символов');
            }
            if (!isPasswordsMatch) {
                errors.push('Пароли не совпадают');
            }
            if (!isConsentGiven) {
                errors.push('Примите условия соглашения и дайте согласие на обработку персональных данных');
            }
            
            if (errors.length > 0) {
                event.preventDefault();
                alert('\n\n• ' + errors.join('\n• '));
            } else if (allFieldsFilled && isNameValid && isEmailValid && isPasswordStrong && isPasswordsMatch && isConsentGiven) {
                // Все поля заполнены корректно и согласие получено
                console.log('Форма валидна, согласие получено, переход на zaivka.html');
                // Раскомментируйте строку ниже для автоматического перехода
                // window.location.href = '/zaivka.html';
            } else {
                event.preventDefault();
            }
        });
    }
});
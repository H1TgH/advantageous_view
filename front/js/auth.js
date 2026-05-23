// js/auth.js - Управление авторизацией и токенами

// Базовый URL API
const API_BASE_URL = 'http://localhost:8000/api/v1';

// ========== УПРАВЛЕНИЕ ТОКЕНАМИ ==========
function saveTokens(accessToken, refreshToken) {
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
    localStorage.setItem('isLoggedIn', 'true');
    localStorage.setItem('loginTime', new Date().toISOString());
}

function getAccessToken() {
    return localStorage.getItem('access_token');
}

function getRefreshToken() {
    return localStorage.getItem('refresh_token');
}

function clearAuth() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('username');
    localStorage.removeItem('loginTime');
}

function isAuthenticated() {
    return localStorage.getItem('isLoggedIn') === 'true' && !!getAccessToken();
}

function getUsername() {
    return localStorage.getItem('username') || 'Пользователь';
}

// ========== API ЗАПРОСЫ ==========
async function apiRequest(endpoint, method = 'GET', body = null, requireAuth = true) {
    const headers = {
        'Content-Type': 'application/json',
    };
    
    if (requireAuth) {
        const token = getAccessToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
    }
    
    const config = {
        method,
        headers,
    };
    
    if (body && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
        config.body = JSON.stringify(body);
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        
        if (response.status === 401 && requireAuth) {
            const refreshed = await refreshAccessToken();
            if (refreshed) {
                return apiRequest(endpoint, method, body, requireAuth);
            } else {
                clearAuth();
                window.location.href = './input.html';
                return null;
            }
        }
        
        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.detail || `Ошибка ${response.status}`);
        }
        
        if (response.status === 204) return null;
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// ========== ОБНОВЛЕНИЕ ТОКЕНА ==========
async function refreshAccessToken() {
    const refreshToken = getRefreshToken();
    if (!refreshToken) return false;
    
    try {
        const response = await fetch(`${API_BASE_URL}/users/refresh`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token: refreshToken })
        });
        
        if (!response.ok) {
            clearAuth();
            return false;
        }
        
        const data = await response.json();
        saveTokens(data.token, refreshToken);
        return true;
    } catch (error) {
        console.error('Refresh error:', error);
        clearAuth();
        return false;
    }
}

// ========== РЕГИСТРАЦИЯ ==========
async function registerUser(userData) {
    return await apiRequest('/users/register', 'POST', userData, false);
}

// ========== ВХОД ==========
async function loginUser(credentials) {
    const response = await apiRequest('/users/login', 'POST', credentials, false);
    
    if (response?.access_token && response?.refresh_token) {
        saveTokens(response.access_token, response.refresh_token);
        localStorage.setItem('username', credentials.email);
        
        const userProfile = {
            email: credentials.email,
            name: credentials.name || credentials.email.split('@')[0],
            password: credentials.password
        };
        localStorage.setItem('userProfile', JSON.stringify(userProfile));
        
        return { success: true, data: response };
    }
    
    return { success: false, message: 'Неверные данные входа' };
}

// ========== ВЫХОД ==========
function logoutUser() {
    clearAuth();
    localStorage.removeItem('userProfile');
    updateVisibilityByAuthStatus();
    updateAuthButton();
    window.location.href = './index.html';
}

// ========== ОБНОВЛЕНИЕ UI ==========
function updateVisibilityByAuthStatus() {
    const isLoggedIn = isAuthenticated();
    
    const navCompare = document.getElementById('compar');
    const navTrack = document.getElementById('track');
    const navHistory = document.getElementById('history');
    const ctaSection = document.getElementById('ctasection');
    
    if (isLoggedIn) {
        if (navCompare) navCompare.style.display = 'list-item';
        if (navTrack) navTrack.style.display = 'list-item';
        if (navHistory) navHistory.style.display = 'list-item';
        if (ctaSection) ctaSection.style.display = 'none';
    } else {
        if (navCompare) navCompare.style.display = 'none';
        if (navTrack) navTrack.style.display = 'none';
        if (navHistory) navHistory.style.display = 'none';
        if (ctaSection) ctaSection.style.display = 'block';
    }
}

function updateButtonToLogin(buttonElement) {
    if (!buttonElement) return;
    buttonElement.innerHTML = '<img src="./img/input.png" style="height: 40px; width: 40px;"> Войти';
    buttonElement.setAttribute('data-status', 'logged-out');
    buttonElement.title = "Войти в аккаунт";
}

// ✅ ИСПРАВЛЕНО: Всегда показываем "Личный кабинет"
function updateButtonToProfile(buttonElement) {
    if (!buttonElement) return;
    buttonElement.innerHTML = '<img src="./img/white-search.png" style="height: 40px; width: 40px;"> Личный кабинет';
    buttonElement.setAttribute('data-status', 'logged-in');
    buttonElement.title = "Перейти в профиль";
}

function updateAuthButton() {
    const button = document.getElementById('userAuthButton');
    if (!button) return;
    
    if (isAuthenticated()) {
        updateButtonToProfile(button);
    } else {
        updateButtonToLogin(button);
    }
    
    button.onclick = function() {
        if (isAuthenticated()) {
            window.location.href = './profile.html';
        } else {
            window.location.href = './input.html';
        }
    };
}

// ========== ИНИЦИАЛИЗАЦИЯ ==========
document.addEventListener('DOMContentLoaded', function() {
    updateAuthButton();
    updateVisibilityByAuthStatus();
    
    window.addEventListener('storage', function(e) {
        if (e.key === 'isLoggedIn' || e.key === 'access_token' || e.key === 'userProfile') {
            updateAuthButton();
            updateVisibilityByAuthStatus();
        }
    });
});

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        apiRequest,
        registerUser,
        loginUser,
        logoutUser,
        isAuthenticated,
        getUsername,
        updateVisibilityByAuthStatus,
        updateAuthButton
    };
}
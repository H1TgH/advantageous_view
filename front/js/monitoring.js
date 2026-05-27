document.addEventListener('DOMContentLoaded', async () => {
    if (localStorage.getItem('isLoggedIn') !== 'true' || !localStorage.getItem('access_token')) {
        window.location.href = './input.html';
        return;
    }

    const listRoot = document.querySelector('.monitoring-list');
    if (!listRoot) {
        return;
    }

    let subscriptions = [];
    let userSettings = null;

    try {
        [subscriptions, userSettings] = await Promise.all([
            apiRequest('/price-tracking/subscriptions'),
            apiRequest('/users/me/notification-settings').catch(() => null),
        ]);
    } catch (error) {
        showToast(error.message || 'Ошибка загрузки мониторинга');
        return;
    }

    renderSubscriptions(listRoot, subscriptions, userSettings);
    await updateUnreadBadge();

    document.addEventListener('click', async (event) => {
        if (event.target.classList.contains('menu-trigger')) {
            const dropdown = event.target.nextElementSibling;
            document.querySelectorAll('.menu-dropdown').forEach(menu => {
                if (menu !== dropdown) {
                    menu.classList.remove('active');
                }
            });
            dropdown.classList.toggle('active');
            return;
        }

        if (event.target.classList.contains('save-price-btn')) {
            const card = event.target.closest('.monitoring-card');
            if (!card) {
                return;
            }
            await saveTargetPrice(card, userSettings);
            return;
        }

        if (event.target.classList.contains('cancel-price-btn')) {
            const card = event.target.closest('.monitoring-card');
            if (!card) {
                return;
            }
            await clearTargetPrice(card, userSettings);
            return;
        }

        if (event.target.classList.contains('delete-item-btn')) {
            const card = event.target.closest('.monitoring-card');
            if (!card) {
                return;
            }
            await deleteSubscription(card);
            if (!document.querySelector('.monitoring-card')) {
                showEmptyState(listRoot);
            }
            return;
        }

        document.querySelectorAll('.menu-dropdown').forEach(menu => {
            menu.classList.remove('active');
        });
    });
});

function renderSubscriptions(root, items, userSettings) {
    root.innerHTML = '';
    if (!items.length) {
        showEmptyState(root);
        return;
    }

    items.forEach(item => {
        const card = document.createElement('article');
        card.className = 'monitoring-card';
        card.dataset.subscriptionId = item.id;
        card.dataset.notifyInApp = String(item.notify_in_app);
        card.dataset.notifyEmail = String(item.notify_email);
        card.innerHTML = `
            <img src="./img/product.png" alt="${escapeHtml(item.title)}" class="product-img">
            <div class="product-info">
                <h3 class="product-name">${escapeHtml(item.title)}</h3>
                <p class="current-price">Текущая цена: <strong>обновляется автоматически</strong></p>
            </div>
            <div class="price-setting">
                <div class="input_price">
                    <label class="price-label">Целевая цена:</label>
                    <input type="number" class="target-price-input" placeholder="Введите цену" value="${item.target_price ?? ''}">
                </div>
                <div class="price-buttons">
                    <button class="save-price-btn">Сохранить</button>
                    <button class="cancel-price-btn ${item.target_price === null ? 'disabled' : ''}" ${item.target_price === null ? 'disabled' : ''}>Отменить</button>
                </div>
                <p class="notification-info">${buildNotifyText(item, userSettings)}</p>
            </div>
            <div class="market-info">
                <img src="${getMarketLogo(item.marketplace)}" alt="${item.marketplace}" class="market-logo">
                <a href="${item.url}" target="_blank" class="details-button">Подробнее →</a>
            </div>
            <div class="menu-container">
                <button class="menu-trigger">⋮</button>
                <div class="menu-dropdown">
                    <button class="delete-item-btn">Удалить</button>
                </div>
            </div>
        `;
        root.appendChild(card);
    });
}

function showEmptyState(root) {
    root.innerHTML = `
        <article class="monitoring-card">
            <div class="product-info">
                <h3 class="product-name">Список мониторинга пуст</h3>
                <p class="current-price">Добавьте товары из поиска через кнопку «Отслеживать»</p>
            </div>
        </article>
    `;
}

async function saveTargetPrice(card, userSettings) {
    const input = card.querySelector('.target-price-input');
    const infoText = card.querySelector('.notification-info');
    const cancelBtn = card.querySelector('.cancel-price-btn');
    const subscriptionId = card.dataset.subscriptionId;
    const targetPrice = input.value.trim();

    if (!targetPrice || Number(targetPrice) <= 0) {
        showToast('Введите корректную цену');
        return;
    }

    try {
        const updated = await apiRequest(`/price-tracking/subscriptions/${subscriptionId}`, 'PATCH', {
            target_price: Number(targetPrice),
        });
        card.dataset.notifyInApp = String(updated.notify_in_app);
        card.dataset.notifyEmail = String(updated.notify_email);
        infoText.textContent = buildNotifyText(updated, userSettings);
        cancelBtn.disabled = false;
        cancelBtn.classList.remove('disabled');
        showToast('Целевая цена сохранена');
    } catch (error) {
        showToast(error.message || 'Не удалось сохранить цену');
    }
}

async function clearTargetPrice(card, userSettings) {
    const input = card.querySelector('.target-price-input');
    const infoText = card.querySelector('.notification-info');
    const cancelBtn = card.querySelector('.cancel-price-btn');
    const subscriptionId = card.dataset.subscriptionId;

    try {
        const updated = await apiRequest(`/price-tracking/subscriptions/${subscriptionId}`, 'PATCH', {
            target_price: null,
        });
        input.value = '';
        card.dataset.notifyInApp = String(updated.notify_in_app);
        card.dataset.notifyEmail = String(updated.notify_email);
        infoText.textContent = buildNotifyText(updated, userSettings);
        cancelBtn.disabled = true;
        cancelBtn.classList.add('disabled');
        showToast('Целевая цена сброшена');
    } catch (error) {
        showToast(error.message || 'Не удалось сбросить цену');
    }
}

async function deleteSubscription(card) {
    const subscriptionId = card.dataset.subscriptionId;
    if (!confirm('Удалить товар?')) {
        return;
    }

    try {
        await apiRequest(`/price-tracking/subscriptions/${subscriptionId}`, 'DELETE');
        card.remove();
        showToast('Товар удален');
    } catch (error) {
        showToast(error.message || 'Не удалось удалить товар');
    }
}

function buildNotifyText(subscription, settings) {
    if (settings && !settings.notifications_enabled) {
        return 'Уведомления отключены в личном кабинете';
    }

    if (settings && !settings.subscription_price_changes) {
        return 'Подписка на изменения цены отключена в личном кабинете';
    }

    const inAppEnabled = subscription.notify_in_app && (!settings || settings.notify_in_app);
    const emailEnabled = subscription.notify_email && (!settings || settings.notify_email);

    if (!inAppEnabled && !emailEnabled) {
        return 'Каналы уведомлений для этого товара отключены';
    }

    if (inAppEnabled && emailEnabled) {
        return 'Уведомления будут приходить на сайте и по email';
    }

    if (emailEnabled) {
        return 'Уведомления будут приходить по email';
    }

    return 'Уведомления будут приходить в «Выгодный взгляд»';
}

async function updateUnreadBadge() {
    const wrapper = document.querySelector('.notification-wrapper');
    if (!wrapper) {
        return;
    }

    try {
        const unread = await apiRequest('/notifications?unread_only=true');
        const count = Array.isArray(unread) ? unread.length : 0;
        const existing = wrapper.querySelector('.notification-badge');
        if (existing) {
            existing.remove();
        }
        if (count > 0) {
            const badge = document.createElement('span');
            badge.className = 'notification-badge';
            badge.textContent = count > 99 ? '99+' : String(count);
            badge.style.cssText = `
                position:absolute;
                top:-6px;
                right:-6px;
                min-width:18px;
                height:18px;
                border-radius:9px;
                background:#e53935;
                color:#fff;
                font-size:11px;
                line-height:18px;
                text-align:center;
                padding:0 4px;
                font-weight:600;
            `;
            wrapper.style.position = 'relative';
            wrapper.appendChild(badge);
        }
    } catch (error) {
        console.error(error);
    }
}

function getMarketLogo(marketplace) {
    if (marketplace === 'wb') {
        return './img/wildberries.png';
    }
    if (marketplace === 'ym') {
        return './img/yandex.png';
    }
    return './img/logo.svg';
}

function escapeHtml(value) {
    return String(value)
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#039;');
}

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
        padding: 12px 24px;
        border-radius: 40px;
        font-size: 14px;
        font-weight: 500;
        z-index: 9999;
    `;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transition = '0.3s';
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, duration);
}

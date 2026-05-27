document.addEventListener('DOMContentLoaded', async function () {
    if (localStorage.getItem('isLoggedIn') !== 'true' || !localStorage.getItem('access_token')) {
        window.location.href = './input.html';
        return;
    }

    const profileBlock = document.getElementById('profileBlock');
    if (profileBlock) {
        profileBlock.style.display = 'block';
    }

    const displayNameSpan = document.getElementById('displayName');
    const displayEmailSpan = document.getElementById('displayEmail');
    const editBtn = document.getElementById('editInfoBtn');
    const modal = document.getElementById('editModal');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const cancelModalBtn = document.getElementById('cancelModalBtn');
    const saveModalBtn = document.getElementById('saveModalBtn');
    const editNameInput = document.getElementById('editName');
    const editEmailInput = document.getElementById('editEmail');
    const notificationToggle = document.getElementById('notificationToggle');
    const notifOffLabel = document.getElementById('notifOffLabel');
    const notifOnLabel = document.getElementById('notifOnLabel');
    const notifyButtons = document.querySelectorAll('.notify-btn');
    const subCheckboxes = document.querySelectorAll('.sub-checkbox');
    const logoutBtn = document.getElementById('logoutBtn');

    let notificationSettings = {
        notifications_enabled: true,
        subscription_price_changes: true,
        subscription_new_features: true,
        notify_in_app: true,
        notify_email: false,
    };

    function updateNotificationLabels(isEnabled) {
        if (isEnabled) {
            notifOffLabel.style.color = '#6c757d';
            notifOnLabel.style.color = '#28a745';
            notifOnLabel.style.fontWeight = '600';
            notifOffLabel.style.fontWeight = '400';
        } else {
            notifOffLabel.style.color = '#dc3545';
            notifOnLabel.style.color = '#6c757d';
            notifOffLabel.style.fontWeight = '600';
            notifOnLabel.style.fontWeight = '400';
        }
    }

    function updateNotifyButtonsState(isEnabled) {
        notifyButtons.forEach(button => {
            button.disabled = !isEnabled;
            button.style.opacity = isEnabled ? '1' : '0.5';
            button.style.cursor = isEnabled ? 'pointer' : 'not-allowed';
        });
    }

    function setNotifyTypeButtons() {
        notifyButtons.forEach(button => button.classList.remove('active'));
        notifyButtons.forEach(button => {
            const text = button.textContent.trim();
            if (text === 'Email' && notificationSettings.notify_email) {
                button.classList.add('active');
            }
            if (text === 'Выгодный взгляд' && notificationSettings.notify_in_app) {
                button.classList.add('active');
            }
        });
    }

    function applySettingsToUI() {
        notificationToggle.checked = notificationSettings.notifications_enabled;
        updateNotificationLabels(notificationSettings.notifications_enabled);
        updateNotifyButtonsState(notificationSettings.notifications_enabled);
        setNotifyTypeButtons();
        if (subCheckboxes[0]) {
            subCheckboxes[0].checked = notificationSettings.subscription_price_changes;
        }
        if (subCheckboxes[1]) {
            subCheckboxes[1].checked = notificationSettings.subscription_new_features;
        }
    }

    async function saveSettings(partial) {
        notificationSettings = { ...notificationSettings, ...partial };
        const channelsSelected = notificationSettings.notify_in_app || notificationSettings.notify_email;
        if (notificationSettings.notifications_enabled && !channelsSelected) {
            notificationSettings.notify_in_app = true;
        }
        try {
            notificationSettings = await apiRequest(
                '/users/me/notification-settings',
                'PATCH',
                notificationSettings
            );
            applySettingsToUI();
        } catch (error) {
            showToast(error.message || 'Не удалось сохранить настройки уведомлений');
        }
    }

    try {
        const [me, settings] = await Promise.all([
            apiRequest('/users/me'),
            apiRequest('/users/me/notification-settings'),
        ]);
        displayNameSpan.textContent = me.name;
        displayEmailSpan.textContent = me.email;
        notificationSettings = settings;
        applySettingsToUI();
    } catch (error) {
        showToast(error.message || 'Не удалось загрузить профиль');
    }

    function openModal() {
        editNameInput.value = displayNameSpan.textContent.trim();
        editEmailInput.value = displayEmailSpan.textContent.trim();
        modal.classList.add('show');
    }

    function closeModal() {
        modal.classList.remove('show');
    }

    async function saveChanges() {
        const newName = editNameInput.value.trim();
        const newEmail = editEmailInput.value.trim();

        if (!newName) {
            showToast('Введите имя');
            return;
        }
        if (!newEmail) {
            showToast('Введите email');
            return;
        }
        const emailPattern = /^[^\s@]+@([^\s@]+\.)+[^\s@]+$/;
        if (!emailPattern.test(newEmail)) {
            showToast('Введите корректный email');
            return;
        }

        try {
            const updated = await apiRequest('/users/me', 'PATCH', {
                name: newName,
                email: newEmail,
            });
            displayNameSpan.textContent = updated.name;
            displayEmailSpan.textContent = updated.email;
            const existingData = JSON.parse(localStorage.getItem('userProfile') || '{}');
            localStorage.setItem('username', updated.email);
            localStorage.setItem('userProfile', JSON.stringify({
                ...existingData,
                name: updated.name,
                email: updated.email,
                updatedAt: new Date().toISOString(),
            }));
            closeModal();
            showToast('Информация успешно обновлена!');
        } catch (error) {
            showToast(error.message || 'Не удалось обновить профиль');
        }
    }

    if (editBtn) {
        editBtn.addEventListener('click', openModal);
    }
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', closeModal);
    }
    if (cancelModalBtn) {
        cancelModalBtn.addEventListener('click', closeModal);
    }
    if (saveModalBtn) {
        saveModalBtn.addEventListener('click', saveChanges);
    }
    if (modal) {
        modal.addEventListener('click', function (e) {
            if (e.target === modal) {
                closeModal();
            }
        });
    }
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal.classList.contains('show')) {
            closeModal();
        }
    });

    if (notificationToggle) {
        notificationToggle.addEventListener('change', async function (e) {
            const isChecked = e.target.checked;
            await saveSettings({ notifications_enabled: isChecked });
            if (isChecked) {
                showToast('Уведомления включены');
            } else {
                showToast('Уведомления выключены');
            }
        });
    }

    notifyButtons.forEach(button => {
        button.addEventListener('click', async () => {
            if (!notificationSettings.notifications_enabled) {
                showToast('Сначала включите уведомления');
                return;
            }
            const buttonText = button.textContent.trim();
            if (buttonText === 'Email') {
                await saveSettings({
                    notify_email: true,
                    notify_in_app: false,
                });
                showToast('Уведомления будут приходить через Email');
                return;
            }
            await saveSettings({
                notify_email: false,
                notify_in_app: true,
            });
            showToast('Уведомления будут приходить в «Выгодный взгляд»');
        });
    });

    if (subCheckboxes[0]) {
        subCheckboxes[0].addEventListener('change', async function (e) {
            await saveSettings({ subscription_price_changes: e.target.checked });
            showToast(e.target.checked ? 'Подписка на изменение цен включена' : 'Подписка на изменение цен выключена');
        });
    }
    if (subCheckboxes[1]) {
        subCheckboxes[1].addEventListener('change', async function (e) {
            await saveSettings({ subscription_new_features: e.target.checked });
            showToast(e.target.checked ? 'Подписка на новые фичи включена' : 'Подписка на новые фичи выключена');
        });
    }

    if (logoutBtn) {
        logoutBtn.addEventListener('click', function () {
            if (confirm('Вы уверены, что хотите выйти?')) {
                localStorage.removeItem('isLoggedIn');
                localStorage.removeItem('username');
                localStorage.removeItem('loginTime');
                localStorage.removeItem('userProfile');
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = './index.html';
            }
        });
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
            z-index: 2000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            pointer-events: none;
        `;
        document.body.appendChild(toast);
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transition = 'opacity 0.3s';
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.remove();
                }
            }, 300);
        }, duration);
    }
});
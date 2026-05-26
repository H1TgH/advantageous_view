// js/profile.js
document.addEventListener('DOMContentLoaded', function () {

    // =========================
    // ПРОВЕРКА АВТОРИЗАЦИИ
    // =========================

    const isLoggedIn =
        localStorage.getItem('isLoggedIn') === 'true';

    if (!isLoggedIn) {
        window.location.href = './input.html';
        return;
    }

    // =========================
    // ПОКАЗЫВАЕМ ПРОФИЛЬ
    // =========================

    const profileBlock =
        document.getElementById('profileBlock');

    if (profileBlock) {
        profileBlock.style.display = 'block';
    }

    // =========================
    // ЭЛЕМЕНТЫ
    // =========================

    const displayNameSpan =
        document.getElementById('displayName');

    const displayEmailSpan =
        document.getElementById('displayEmail');

    const editBtn =
        document.getElementById('editInfoBtn');

    const modal =
        document.getElementById('editModal');

    const closeModalBtn =
        document.getElementById('closeModalBtn');

    const cancelModalBtn =
        document.getElementById('cancelModalBtn');

    const saveModalBtn =
        document.getElementById('saveModalBtn');

    const editNameInput =
        document.getElementById('editName');

    const editEmailInput =
        document.getElementById('editEmail');

    // =========================
    // ЗАГРУЗКА ДАННЫХ
    // =========================

    function loadUserData() {

        const userProfile =
            JSON.parse(
                localStorage.getItem('userProfile') || '{}'
            );

        const username =
            localStorage.getItem('username') || '';

        // Имя
        if (
            userProfile.name &&
            userProfile.name.trim() !== ''
        ) {

            displayNameSpan.textContent =
                userProfile.name;

        } else {

            displayNameSpan.textContent =
                username.split('@')[0] || 'Пользователь';

        }

        // Email
        if (
            userProfile.email &&
            userProfile.email.trim() !== ''
        ) {

            displayEmailSpan.textContent =
                userProfile.email;

        } else {

            displayEmailSpan.textContent =
                username;

        }

    }

    loadUserData();

    // =========================
    // СОХРАНЕНИЕ ДАННЫХ
    // =========================

    function saveUserData() {

        const userProfile = {

            name:
                displayNameSpan.textContent.trim(),

            email:
                displayEmailSpan.textContent.trim(),

            updatedAt:
                new Date().toISOString()

        };

        const existingData =
            JSON.parse(
                localStorage.getItem('userProfile') || '{}'
            );

        if (existingData.password) {
            userProfile.password =
                existingData.password;
        }

        localStorage.setItem(
            'userProfile',
            JSON.stringify(userProfile)
        );

        localStorage.setItem(
            'username',
            userProfile.email
        );

    }

    // =========================
    // МОДАЛКА
    // =========================

    function openModal() {

        editNameInput.value =
            displayNameSpan.textContent.trim();

        editEmailInput.value =
            displayEmailSpan.textContent.trim();

        modal.classList.add('show');

    }

    function closeModal() {
        modal.classList.remove('show');
    }

    function saveChanges() {

        const newName =
            editNameInput.value.trim();

        const newEmail =
            editEmailInput.value.trim();

        if (!newName) {
            showToast('Введите имя');
            return;
        }

        if (!newEmail) {
            showToast('Введите email');
            return;
        }

        const emailPattern =
            /^[^\s@]+@([^\s@]+\.)+[^\s@]+$/;

        if (!emailPattern.test(newEmail)) {

            showToast(
                'Введите корректный email'
            );

            return;
        }

        displayNameSpan.textContent =
            newName;

        displayEmailSpan.textContent =
            newEmail;

        saveUserData();

        closeModal();

        showToast(
            'Информация успешно обновлена!'
        );

    }

    // =========================
    // СОБЫТИЯ МОДАЛКИ
    // =========================

    if (editBtn) {
        editBtn.addEventListener(
            'click',
            openModal
        );
    }

    if (closeModalBtn) {
        closeModalBtn.addEventListener(
            'click',
            closeModal
        );
    }

    if (cancelModalBtn) {
        cancelModalBtn.addEventListener(
            'click',
            closeModal
        );
    }

    if (saveModalBtn) {
        saveModalBtn.addEventListener(
            'click',
            saveChanges
        );
    }

    if (modal) {

        modal.addEventListener(
            'click',
            function (e) {

                if (e.target === modal) {
                    closeModal();
                }

            }
        );

    }

    // =========================
    // ESC
    // =========================

    document.addEventListener(
        'keydown',
        function (e) {

            if (
                e.key === 'Escape' &&
                modal.classList.contains('show')
            ) {

                closeModal();

            }

        }
    );

    // =========================
    // УВЕДОМЛЕНИЯ
    // =========================

    const notificationToggle =
        document.getElementById(
            'notificationToggle'
        );

    const notifOffLabel =
        document.getElementById(
            'notifOffLabel'
        );

    const notifOnLabel =
        document.getElementById(
            'notifOnLabel'
        );

    const notifyButtons =
        document.querySelectorAll(
            '.notify-btn'
        );

    // =========================
    // LABEL
    // =========================

    function updateNotificationLabels(
        isEnabled
    ) {

        if (isEnabled) {

            notifOffLabel.style.color =
                '#6c757d';

            notifOnLabel.style.color =
                '#28a745';

            notifOnLabel.style.fontWeight =
                '600';

            notifOffLabel.style.fontWeight =
                '400';

        } else {

            notifOffLabel.style.color =
                '#dc3545';

            notifOnLabel.style.color =
                '#6c757d';

            notifOffLabel.style.fontWeight =
                '600';

            notifOnLabel.style.fontWeight =
                '400';

        }

    }
    function updateNotifyButtonsState(isEnabled) {

        notifyButtons.forEach(button => {

            if (isEnabled) {

                button.disabled = false;
                button.style.opacity = '1';
                button.style.cursor = 'pointer';

            } else {

                button.disabled = true;
                button.style.opacity = '0.5';
                button.style.cursor = 'not-allowed';

                // Убираем active
                button.classList.remove('active');

            }

        });

    }

    // =========================
    // ЗАГРУЗКА СОСТОЯНИЯ
    // =========================

    const savedNotif =
        localStorage.getItem(
            'notificationsEnabled'
        );

    if (savedNotif !== null) {

        const isEnabled =
            savedNotif === 'true';

        notificationToggle.checked =
            isEnabled;

        updateNotificationLabels(
            isEnabled
        );

        updateNotifyButtonsState(
            isEnabled
        );

    }

    // =========================
    // ПЕРЕКЛЮЧАТЕЛЬ
    // =========================

    if (notificationToggle) {

        notificationToggle.addEventListener(
            'change',
            function (e) {

                const isChecked =
                    e.target.checked;

                localStorage.setItem(
                    'notificationsEnabled',
                    isChecked
                );

                updateNotificationLabels(
                    isChecked
                );

                updateNotifyButtonsState(
                    isChecked
                );

                if (isChecked) {

                    const notifyType =
                        localStorage.getItem(
                            'notifyType'
                        ) || 'website';

                    showToast(
                        `Уведомления будут приходить через ${notifyType === 'email'
                            ? 'Email'
                            : 'Выгодный взгляд'
                        }`
                    );

                } else {

                    showToast(
                        'Включите уведомления для получения сообщений'
                    );

                }

            }
        );

    }

    // =========================
    // СПОСОБ УВЕДОМЛЕНИЙ
    // =========================

    const savedNotifyType =
        localStorage.getItem(
            'notifyType'
        ) || 'website';

    notifyButtons.forEach(button => {

        const buttonText =
            button.textContent.trim();

        // Активная кнопка
        if (
            buttonText === 'Email' &&
            savedNotifyType === 'email'
        ) {

            button.classList.add('active');

        }

        if (
            buttonText === 'Выгодный взгляд' &&
            savedNotifyType === 'website'
        ) {

            button.classList.add('active');

        }

        // Клик
        button.addEventListener(
            'click',
            () => {

                notifyButtons.forEach(btn =>
                    btn.classList.remove('active')
                );

                button.classList.add('active');

                const type =
                    buttonText === 'Email'
                        ? 'email'
                        : 'website';

                localStorage.setItem(
                    'notifyType',
                    type
                );

                const notificationsEnabled =
                    localStorage.getItem(
                        'notificationsEnabled'
                    ) === 'true';

                if (!notificationsEnabled) {

                    showToast(
                        'Сначала включите уведомления'
                    );

                    return;
                }

                showToast(
                    `Уведомления будут приходить через ${type === 'email'
                        ? 'Email'
                        : 'Выгодный взгляд'
                    }`
                );

            }
        );

    });

    // =========================
    // ПОДПИСКИ
    // =========================

    const subCheckboxes =
        document.querySelectorAll(
            '.sub-checkbox'
        );

    const savedSubs =
        localStorage.getItem(
            'subscriptionsState'
        );

    if (savedSubs) {

        try {

            const states =
                JSON.parse(savedSubs);

            subCheckboxes.forEach(
                (checkbox, index) => {

                    if (
                        states[index] !== undefined
                    ) {

                        checkbox.checked =
                            states[index];

                    }

                }
            );

        } catch (e) { }

    }

    subCheckboxes.forEach(
        checkbox => {

            checkbox.addEventListener(
                'change',
                function () {

                    const states = [];

                    subCheckboxes.forEach(
                        cb => states.push(cb.checked)
                    );

                    localStorage.setItem(
                        'subscriptionsState',
                        JSON.stringify(states)
                    );

                }
            );

        }
    );

    // =========================
    // ВЫХОД
    // =========================

    const logoutBtn =
        document.getElementById('logoutBtn');

    if (logoutBtn) {

        logoutBtn.addEventListener(
            'click',
            function () {

                if (
                    confirm(
                        'Вы уверены, что хотите выйти?'
                    )
                ) {

                    localStorage.removeItem(
                        'isLoggedIn'
                    );

                    localStorage.removeItem(
                        'username'
                    );

                    localStorage.removeItem(
                        'loginTime'
                    );

                    localStorage.removeItem(
                        'userProfile'
                    );

                    localStorage.removeItem(
                        'access_token'
                    );

                    localStorage.removeItem(
                        'refresh_token'
                    );

                    window.location.href =
                        './index.html';

                }

            }
        );

    }

    // =========================
    // TOAST
    // =========================

    function showToast(
        message,
        duration = 2500
    ) {

        const existingToast =
            document.querySelector(
                '.custom-toast'
            );

        if (existingToast) {
            existingToast.remove();
        }

        const toast =
            document.createElement('div');

        toast.className =
            'custom-toast';

        toast.textContent =
            message;

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
            toast.style.transition =
                'opacity 0.3s';

            setTimeout(() => {

                if (toast.parentNode) {
                    toast.remove();
                }

            }, 300);

        }, duration);

    }

    console.log(
        '✅ Личный кабинет загружен'
    );

});
//monitoring.js
document.addEventListener('DOMContentLoaded', () => {

    // =========================
    // СОХРАНЕНИЕ ЦЕНЫ
    // =========================

    const saveButtons =
        document.querySelectorAll('.save-price-btn');

    saveButtons.forEach(button => {

        button.addEventListener('click', () => {

            const card =
                button.closest('.monitoring-card');

            const input =
                card.querySelector('.target-price-input');

            const infoText =
                card.querySelector('.notification-info');

            const targetPrice =
                input.value.trim();

            // Проверка цены
            if (!targetPrice || Number(targetPrice) <= 0) {

                showToast('Введите корректную цену');

                return;
            }

            // Проверка уведомлений
            const notificationsEnabled =
                localStorage.getItem('notificationsEnabled') === 'true';

            // Если выключены
            if (!notificationsEnabled) {

                infoText.textContent =
                    'Включите уведомления в личном кабинете';

                showToast(
                    'Для отслеживания включите уведомления'
                );

                return;
            }

            // Тип уведомлений
            const notifyType =
                localStorage.getItem('notifyType') || 'website';

            // Email
            const userProfile =
                JSON.parse(
                    localStorage.getItem('userProfile') || '{}'
                );

            // Сообщение
            if (notifyType === 'email') {

                infoText.textContent =
                    `Уведомления будут приходить на ${userProfile.email || 'ваш email'}`;

            } else {

                infoText.textContent =
                    'Уведомления будут приходить в «Выгодный взгляд»';

            }

            // Название товара
            const productName =
                card.querySelector('.product-name').textContent;

            // Сохранение
            const monitoringItem = {
                product: productName,
                targetPrice: targetPrice,
                notifyType: notifyType,
                createdAt: new Date().toISOString()
            };

            localStorage.setItem(
                'lastMonitoring',
                JSON.stringify(monitoringItem)
            );

            showToast('Цена сохранена');
            // Активируем кнопку отмены
            const cancelBtn =
                card.querySelector('.cancel-price-btn');

            cancelBtn.disabled = false;

            cancelBtn.classList.remove('disabled');


        });

    });
    // =========================
    // ОТМЕНА
    // =========================

    // =========================
    // ОТМЕНА
    // =========================

    // =========================
    // ОТМЕНА
    // =========================

    const cancelButtons =
        document.querySelectorAll('.cancel-price-btn');

    cancelButtons.forEach(button => {

        // Изначально кнопка выключена
        button.disabled = true;
        button.classList.add('disabled');

        button.addEventListener('click', () => {

            // Если кнопка выключена
            if (button.disabled) return;

            const card =
                button.closest('.monitoring-card');

            const infoText =
                card.querySelector('.notification-info');

            // Убираем сообщение
            infoText.textContent = '';

            // Делаем кнопку снова неактивной
            button.disabled = true;

            button.classList.add('disabled');

            showToast(
                'Цена больше не отслеживается',
                1500
            );

        });

    });

    // =========================
    // МЕНЮ
    // =========================

    document.addEventListener('click', (event) => {

        // Открытие меню
        if (event.target.classList.contains('menu-trigger')) {

            const dropdown =
                event.target.nextElementSibling;

            document.querySelectorAll('.menu-dropdown')
                .forEach(menu => {

                    if (menu !== dropdown) {
                        menu.classList.remove('active');
                    }

                });

            dropdown.classList.toggle('active');
        }

        // Удаление
        else if (
            event.target.classList.contains('delete-item-btn')
        ) {

            const card =
                event.target.closest('.monitoring-card');

            if (confirm('Удалить товар?')) {

                card.remove();

                showToast('Товар удален');
            }
        }

        // Закрытие меню
        else {

            document.querySelectorAll('.menu-dropdown')
                .forEach(menu => {
                    menu.classList.remove('active');
                });

        }

    });

});


// =========================
// TOAST
// =========================

function showToast(message, duration = 2500) {

    const existingToast =
        document.querySelector('.custom-toast');

    if (existingToast) {
        existingToast.remove();
    }

    const toast =
        document.createElement('div');

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

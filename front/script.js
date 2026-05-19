document.addEventListener('click', (event) => {
    // 1. Логика открытия/закрытия меню
    if (event.target.classList.contains('menu-trigger')) {
        const dropdown = event.target.nextElementSibling;
        // Закрываем другие открытые меню (опционально)
        document.querySelectorAll('.menu-dropdown').forEach(m => {
            if (m !== dropdown) m.classList.remove('active');
        });
        dropdown.classList.toggle('active');
    }

    // 2. Логика удаления карточки
    else if (event.target.classList.contains('delete-item-btn')) {
        const card = event.target.closest('.monitoring-card');
        if (confirm('Вы уверены, что хотите удалить этот товар?')) {
            card.remove();
        }
    }

    // 3. Закрытие меню при клике в пустое место
    else {
        document.querySelectorAll('.menu-dropdown').forEach(m => m.classList.remove('active'));
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const sliders = document.querySelectorAll('.price-slider');

    sliders.forEach(slider => {
        slider.addEventListener('input', function () {
            // находим текущую карточку
            const card = this.closest('.monitoring-card');

            // находим элемент с ценой внутри этой карточки
            const priceLabel = card.querySelector('.price-value');

            // форматируем число (65 000 ₽)
            const value = Number(this.value).toLocaleString('ru-RU') + ' ₽';

            // обновляем текст
            priceLabel.textContent = value;
        });
    });
});
// ===== CONFIG =====

const API_BASE = 'http://127.0.0.1:8000/api/v1';

let currentProducts = [];


// ===== INIT =====

document.addEventListener('DOMContentLoaded', () => {

    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');

    // ENTER

    searchInput.addEventListener('keypress', (e) => {

        if (e.key === 'Enter') {
            performSearch();
        }

    });

    // BUTTON

    searchButton.addEventListener('click', performSearch);

    // FILTERS

    document.getElementById('priceFrom')
        .addEventListener('input', applyFilters);

    document.getElementById('priceTo')
        .addEventListener('input', applyFilters);

    document.getElementById('freeDelivery')
        .addEventListener('change', applyFilters);

    document.querySelectorAll('input[name="speed"]')
        .forEach(radio => {

            radio.addEventListener('change', applyFilters);

        });

    // SORT

    document.querySelectorAll('.sort-list li')
        .forEach(item => {

            item.addEventListener('click', () => {

                const sort = item.dataset.sort;

                sortProducts(sort);

                renderResults(currentProducts);

            });

        });

});


// ===== SEARCH =====

async function performSearch() {

    const query = document
        .getElementById('searchInput')
        .value
        .trim();

    if (!query) {

        alert('Введите запрос');

        return;
    }

    showLoader();

    try {

        const response = await fetch(
            `${API_BASE}/search/?query=${encodeURIComponent(query)}`
        );

        if (!response.ok) {
            throw new Error('Ошибка сервера');
        }

        const products = await response.json();

        currentProducts = products;

        applyFilters();

    }

    catch (error) {

        console.error(error);

        hideLoader();

        alert('Ошибка загрузки');

    }

}


// ===== FILTERS =====

function applyFilters() {

    let filtered = [...currentProducts];

    // PRICE

    const minPrice =
        parseFloat(document.getElementById('priceFrom').value) || 0;

    const maxPrice =
        parseFloat(document.getElementById('priceTo').value) || Infinity;

    filtered = filtered.filter(product => {

        const total =
            product.price + (product.delivery_price || 0);

        return total >= minPrice && total <= maxPrice;

    });

    // DELIVERY

    const speed =
        document.querySelector('input[name="speed"]:checked');

    if (speed) {

        const days = parseInt(speed.value);

        filtered = filtered.filter(product => {

            return product.delivery_days <= days;

        });

    }

    // FREE DELIVERY

    if (document.getElementById('freeDelivery').checked) {

        filtered = filtered.filter(product => {

            return product.delivery_free === true;

        });

    }

    renderResults(filtered);

}


// ===== SORT =====

function sortProducts(type) {

    switch (type) {

        case 'price':

            currentProducts.sort((a, b) => {

                return a.price - b.price;

            });

            break;

        case 'delivery':

            currentProducts.sort((a, b) => {

                return a.delivery_days - b.delivery_days;

            });

            break;

        case 'rating':

            currentProducts.sort((a, b) => {

                return b.rating - a.rating;

            });

            break;

        default:

            break;

    }

}


// ===== RENDER =====

function renderResults(products) {

    hideLoader();

    const emptySection =
        document.getElementById('emptySection');

    const resultsSection =
        document.getElementById('resultsSection');

    const tbody =
        document.getElementById('offersTableBody');

    emptySection.style.display = 'none';

    resultsSection.style.display = 'block';

    tbody.innerHTML = '';

    if (!products.length) {

        tbody.innerHTML = `
            <tr>
                <td colspan="6">
                    Ничего не найдено
                </td>
            </tr>
        `;

        return;
    }

    products.forEach(product => {

        const row = document.createElement('tr');

        row.innerHTML = `

            <td>
                <img
                    src="${getMarketplaceLogo(product.marketplace)}"
                    class="market-logo"
                    alt=""
                >
            </td>

            <td>

                <div class="seller-info">

                    <span class="seller-name">
                        ${product.seller}
                    </span>

                    <span class="seller-rating">
                        ⭐ ${product.rating}
                    </span>

                </div>

            </td>

            <td>

                <div class="price-block">

                    <span class="price-value">
                        ${formatPrice(product.price)} ₽
                    </span>

                </div>

            </td>

            <td>

                <div class="delivery-info">

                    <span class="delivery-date">
                        ${formatDelivery(product.delivery_days)}
                    </span>

                    ${
                        product.delivery_free
                            ? '<span class="delivery-status free">Бесплатно</span>'
                            : `<span>${product.delivery_price} ₽</span>`
                    }

                </div>

            </td>

            <td>

                <span class="total-rating">
                    ⭐ ${product.rating}
                </span>

            </td>

            <td>

                <div class="action-block">

                    <a
                        href="${product.url}"
                        target="_blank"
                        class="market-link"
                    >
                        Перейти →
                    </a>

                </div>

            </td>

        `;

        tbody.appendChild(row);

    });

}


// ===== UI =====

function showLoader() {

    document.getElementById('loaderSection')
        .style.display = 'block';

    document.getElementById('resultsSection')
        .style.display = 'none';

}


function hideLoader() {

    document.getElementById('loaderSection')
        .style.display = 'none';

}


// ===== HELPERS =====

function formatPrice(price) {

    return new Intl.NumberFormat('ru-RU')
        .format(price);

}


function formatDelivery(days) {

    if (days <= 1) {
        return 'Завтра';
    }

    if (days <= 2) {
        return 'Послезавтра';
    }

    return `${days} дн.`;

}


function getMarketplaceLogo(marketplace) {

    switch (marketplace) {

        case 'wb':
            return './img/wildberries.png';

        case 'ozon':
            return './img/ozon.png';

        case 'ym':
            return './img/yandex.png';

        default:
            return './img/logo.svg';

    }

}
// ===== AUTO SEARCH FROM INDEX =====

document.addEventListener('DOMContentLoaded', () => {

    const params = new URLSearchParams(
        window.location.search
    );

    const query = params.get('query');

    if (query) {

        const input =
            document.getElementById('searchInput');

        input.value = query;

        performSearch();

    }

});
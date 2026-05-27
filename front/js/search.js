//saerch.js
const searchBtn = document.getElementById("searchBtn");
const searchInput = document.getElementById("searchInput");
const productsContainer = document.getElementById("products");


searchBtn.addEventListener("click", async () => {

    const query = searchInput.value.trim();

    if (!query) {
        alert("Введите запрос");
        return;
    }

    productsContainer.innerHTML = "<p>Загрузка...</p>";

    try {

        const response = await fetch(
            `${API_URL}/search?query=${encodeURIComponent(query)}`
        );

        if (!response.ok) {
            throw new Error("Ошибка поиска");
        }

        const products = await response.json();

        renderProducts(products);

    } catch (error) {

        console.error(error);

        productsContainer.innerHTML =
            "<p>Ошибка загрузки товаров</p>";
    }
});


function renderProducts(products) {

    productsContainer.innerHTML = "";

    if (!products.length) {

        productsContainer.innerHTML =
            "<p>Ничего не найдено</p>";

        return;
    }

    products.forEach(product => {

        const card = document.createElement("div");

        card.className = "product-card";

        card.innerHTML = `
            <img src="${product.image_url}" alt="${product.title}">

            <h3>${product.title}</h3>

            <p>${product.price} ₽</p>

            <a href="${product.url}" target="_blank">
                Открыть товар
            </a>

            <button onclick='trackPrice(${JSON.stringify(product)})'>
                Следить за ценой
            </button>
        `;

        productsContainer.appendChild(card);
    });
}

async function trackPrice(product) {

    const token = localStorage.getItem('access_token');

    if (!token) {

        alert('Войдите в аккаунт');

        return;

    }

    try {

        const response = await fetch(
            `http://127.0.0.1:8000/api/v1/price-tracking/subscriptions`,
            {
                method: 'POST',

                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },

                body: JSON.stringify({

                    product_id: String(
                        product.product_id ||
                        product.id ||
                        product.url
                    ),

                    title: product.title || 'Товар',

                    url: product.url,

                    marketplace: product.marketplace || 'wb',

                    current_price: Number(product.price),

                    target_price: Number(product.price) - 1000,

                    notify_in_app: true,

                    notify_email: true

                })

            }
        );

        const data = await response.json();

        if (!response.ok) {

            alert(data.detail || 'Ошибка подписки');

            return;

        }

        alert('Товар добавлен в отслеживание');

    }

    catch (error) {

        console.error(error);

        alert('Ошибка соединения');

    }

}
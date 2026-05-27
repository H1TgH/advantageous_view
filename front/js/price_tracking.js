async function subscribeToPrice(
    productId,
    title,
    url,
    marketplace,
    currentPrice
) {

    const token = localStorage.getItem("access_token");

    if (!token) {

        alert("Сначала войдите в аккаунт");

        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/price-tracking/subscriptions`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },

                body: JSON.stringify({
                    product_id: productId,
                    title: title,
                    url: url,
                    marketplace: marketplace,
                    current_price: currentPrice,
                    target_price: null,
                    notify_in_app: true,
                    notify_email: false
                })
            }
        );

        if (response.ok) {

            alert("Подписка оформлена");

        } else {

            const error = await response.json();

            alert(error.detail || "Ошибка");
        }

    } catch (error) {

        console.error(error);

        alert("Ошибка сервера");
    }
}
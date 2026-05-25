// ===== CONFIG =====

const searchInput = document.getElementById('searchInput');

const searchBtn = document.getElementById('searchBtn');

const chips = document.querySelectorAll('.chip');


// ===== SEARCH =====

function goToComparePage(query) {

    if (!query || !query.trim()) {

        alert('Введите запрос');

        return;

    }

    // сохраняем запрос
    localStorage.setItem(
        'searchQuery',
        query.trim()
    );

    // переход
    window.location.href =
        `compare.html?query=${encodeURIComponent(query)}`;
}


// ===== BUTTON =====

searchBtn.addEventListener('click', () => {

    const query = searchInput.value;

    goToComparePage(query);

});


// ===== ENTER =====

searchInput.addEventListener('keypress', (e) => {

    if (e.key === 'Enter') {

        goToComparePage(searchInput.value);

    }

});


// ===== POPULAR CHIPS =====

chips.forEach(chip => {

    chip.addEventListener('click', () => {

        const query =
            chip.dataset.query;

        // вставляем в input
        searchInput.value = query;

        // переход
        goToComparePage(query);

    });

});
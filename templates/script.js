function searchItems() {
    let search_text = document.getElementById('search_text').value;

    if (search_text.trim().length === 0) {
        document.getElementById('search_results').innerHTML = '';
        return;
    }

    fetch(`/search?q=${search_text}`)
        .then(response => response.json())
        .then(data => {
            let searchResults = document.getElementById('search_results');
            searchResults.innerHTML = '';

            data.forEach(item => {
                let li = document.createElement('li');
                li.textContent = item.title;
                
                li.addEventListener('click', () => {
                    // Действие при выборе товара
                    alert(`Выбран товар: ${item.title}`);
                });

                searchResults.appendChild(li);
            });
        })
        .catch(error => console.error(error));
}
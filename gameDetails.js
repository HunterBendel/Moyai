// Function to fetch game details from an API
function fetchGameDetails(gameId) {
    // Example API endpoint (replace with your actual endpoint)
    const apiUrl = `https://your-api.com/games/${gameId}`;

    fetch(apiUrl)
        .then(response => response.json())
        .then(game => {
            // Update the HTML elements with the game details
            document.getElementById('game-info').querySelector('h2').textContent = game.name;
            document.getElementById('game-image').src = game.imageUrl;
            document.getElementById('game-info').querySelectorAll('p')[0].textContent = `Genre: ${game.genre}`;
            document.getElementById('game-info').querySelectorAll('p')[1].textContent = `Description: ${game.description}`;
            // Add more details as needed
        })
        .catch(error => {
            console.error('Error fetching game details:', error);
        });
}

// Example usage (replace '123' with the actual game ID)
fetchGameDetails(123);

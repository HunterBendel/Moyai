// A JavaScript file for adding interactivity to our website if we need it
// Function to simulate game search
function searchGames() {
    const searchInput = document.getElementById('game-search').value;
    if (searchInput.trim() === '') {
        alert('Please enter a game name to search.');
        return;
    }

    // For demonstration purposes, this will just display an alert
    // In a real application, you would make an API call to search for games
    alert('Searching for games related to: ' + searchInput);
}

// Example function to display recommended games (static data for demonstration)
function displayRecommendedGames() {
    const recommendedGamesContainer = document.getElementById('recommended-games');
    const games = ['Game 1', 'Game 2', 'Game 3']; // Sample game data

    games.forEach(game => {
        const gameElement = document.createElement('div');
        gameElement.textContent = game;
        recommendedGamesContainer.appendChild(gameElement);
    });
}

// Call the function to display recommended games on page load
window.onload = function() {
    displayRecommendedGames();
};

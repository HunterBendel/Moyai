// Sample search results
const searchResults = [
    { name: "Game 1", genre: "Action", description: "Description of Game 1" },
    { name: "Game 2", genre: "Adventure", description: "Description of Game 2" },
    // Add more game objects as needed
];

// Function to display search results on a single page
function displaySearchResults(results) {
    const resultsContainer = document.getElementById("search-results");
    resultsContainer.innerHTML = ""; // Clear previous results

    results.forEach(game => {
        const gameElement = document.createElement("div");
        gameElement.classList.add("game-result");
        gameElement.innerHTML = `
            <h3>${game.name}</h3>
            <p>Genre: ${game.genre}</p>
            <p>${game.description}</p>
        `;
        resultsContainer.appendChild(gameElement);
    });
}

// Call the function to display search results
displaySearchResults(searchResults);

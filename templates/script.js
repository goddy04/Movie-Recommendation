// script.js

// When the form is submitted
document.getElementById('movieForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Get the movie name and rating from the form inputs
    const movieName = document.getElementById('movieName').value;
    const rating = document.getElementById('rating').value;

    // Send movie data to the backend via an API call
    fetch('/store-movie', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ movieName: movieName, rating: rating }),
    })
    .then(response => response.json())
    .then(data => {
        // Update the movie history on the page
        const movieHistory = document.getElementById('movieHistory');
        const li = document.createElement('li');
        li.textContent = `${movieName} (Rating: ${rating})`;
        movieHistory.appendChild(li);

        // Fetch new recommendations after updating movie history
        fetchRecommendations();
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Function to fetch movie recommendations from the backend
function fetchRecommendations() {
    fetch('/get-recommendations', {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        // Display recommendations
        const recommendationsDiv = document.getElementById('recommendations');
        recommendationsDiv.innerHTML = data.recommendations;
    })
    .catch(error => {
        console.error('Error fetching recommendations:', error);
    });
}

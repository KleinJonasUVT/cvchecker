document.getElementById('CV_form').onsubmit = function(event) {
    event.preventDefault();

    const container = document.querySelector('#result');
    container.innerHTML = ''; // Clear the container before adding new items

    // Show loader
    const loadings = document.querySelectorAll('.loading');
    loadings.forEach(function(loading) {
        loading.style.display = 'block'; // Set display to 'block'
    });

    // Collect form data
    const formData = new FormData(event.target);

    // Send data to Flask backend
    fetch('/data', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // Hide loader
        loadings.forEach(function(loading) {
            loading.style.display = 'none'; // Set display to 'none'
        });

        // Check if there's an error
        if (data.error) {
            container.innerHTML = `<div class="error-message">${data.error}</div>`;
            return;
        }

        // Assuming container is defined earlier or exists in your HTML
        const container = document.querySelector('#result');
        container.innerHTML = `<div class="sent-message"><p>${data.result}</p></div>`;
    })
    .catch(error => {
        console.error('Error:', error);
        container.innerHTML = `<div class="error-message">An error occurred. Please try again later.</div>`;
        loadings.forEach(function(loading) {
            loading.style.display = 'none'; // Set display to 'none'
        });
    });
};




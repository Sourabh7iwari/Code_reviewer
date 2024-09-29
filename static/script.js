
document.getElementById('codeForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    let code = document.getElementById('code').value;
    let language = document.getElementById('language').value;
    let feedbackElement = document.getElementById('feedback');
    let loadingElement = document.getElementById('loading');

    feedbackElement.innerHTML = '';
    loadingElement.style.display = 'block';

    fetch('/submit_code', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `code=${encodeURIComponent(code)}&language=${encodeURIComponent(language)}`,
    })
    .then(response => response.json())
    .then(data => {
        loadingElement.style.display = 'none';
        feedbackElement.innerHTML = data.feedback;
    })
    .catch(error => {
        loadingElement.style.display = 'none';
        feedbackElement.innerHTML = '<p>Error: Something went wrong. Please try again.</p>';
    });
});

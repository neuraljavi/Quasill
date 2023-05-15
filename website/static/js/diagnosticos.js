document.querySelector('.btnDiagnosis').addEventListener('click', function(event) {
    event.preventDefault(); // Prevent form submission

    var textarea = document.getElementById('inputSintomas');
    var text = textarea.value;

    fetch('/diagnostico', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'inputSintomas': text
        })
    })
    .then(function(response) {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Error: ' + response.status);
        }
    })
    .then(function(data) {
        // Update the result container with the predicted illnesses
        var diseaseDataElement = document.getElementById('disease-data');
        diseaseDataElement.textContent = data.predicted_illnesses;

        // Optionally, you can update other elements in the result container as well
        var probabilityDataElement = document.getElementById('probability-data');
        probabilityDataElement.textContent = data.probability;
        // Finally, you may want to hide the textarea or clear its value after getting the result
        textarea.style.display = 'none';
        textarea.value = '';
    })
    .catch(function(error) {
        console.error(error);
    });
});

function getCurrentDate() {
    // Implement a function to get the current date in the desired format
    // Example implementation: return new Date().toLocaleDateString();
    return '15/11/2054'; // Replace with the appropriate implementation
}

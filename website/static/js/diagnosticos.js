document.querySelector('.btnDiagnosis').addEventListener('click', function (event) {
    var textarea = document.getElementById('inputSintomas');
    var text = textarea.value;

    // Realizamos una solicitud POST a "/diagnostico"
    fetch('/diagnostico', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            'inputSintomas': text
        })
    })
        .then(function (response) {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Error: ' + response.status);
            }
        })
        .then(function (data) {
            // Redireccionamos a la página de resultados
            location.href = '/resultados.html';
        })
        .catch(function (error) {
            console.error(error);
        });
});

function preventNewline(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
    }
}

function checkWordCount() {
    var textarea = document.getElementById('inputSintomas');
    var wordCount = textarea.value.split(/\s+/).filter(function(word) {
        return /\S/.test(word);
    }).length;

    var button = document.querySelector('.btnDiagnosis');
    if (wordCount < 5) {
        button.disabled = true;
    } else {
        button.disabled = false;
    }
}


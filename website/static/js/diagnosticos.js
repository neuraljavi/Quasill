// FUNCIÓN CREADA POR ALEJANDRA
document.querySelector('.btnDiagnosis').addEventListener('click', function (event) {
    var textarea = document.getElementById('inputSintomas');
    var text = textarea.value;

    // Realizamos una solicitud POST a "/diagnostico"
    fetch('/diagnostico', {
        method: 'POST',
        headers: {
            //Cómo interpreta los datos el servidor
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
            // Redireccionamos a resultados si OK
            location.href = '/resultados.html';
        })
});

// FUNCIONES CREADAS POR JAVIER

function preventNewline(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
    }
}

function checkWordCount() {
    var textarea = document.getElementById('inputSintomas');
    var wordCount = textarea.value.split(/\s+/).filter(function (word) {
        return /\S/.test(word);
    }).length;

    var button = document.querySelector('.btnDiagnosis');
    if (wordCount < 5) {
        button.disabled = true;
    } else {
        button.disabled = false;
    }
}


document.querySelector('.btnDiagnosis').addEventListener('click', function (event) {
    var textarea = document.getElementById('inputSintomas');
    var text = textarea.value;

    // Realizar una solicitud POST al endpoint "/diagnostico"
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
            // Redirigir a la página de resultados después de obtener el diagnóstico
            location.href = '/resultados.html';
        })
        .catch(function (error) {
            console.error(error);
        });
});

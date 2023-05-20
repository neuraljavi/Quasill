// Obtiene el ID de diagnóstico de la URL
const urlParams = new URLSearchParams(window.location.search);
const diagId = urlParams.get('diag_id');

// Cuando se envía el formulario, envía una solicitud PUT a actualizar_diagnostico
document.querySelector('.feedback-form').addEventListener('submit', function(e) {
    e.preventDefault();

    // Obtiene la enfermedad seleccionada y los comentarios adicionales
    const selectedDisease = document.querySelector('.lista-enfermedades').value;
    const feedback = document.querySelector('#inputFeedback').value;

    // Crea un objeto con los datos que se enviarán
    const data = {
        'correct_label': selectedDisease,
        'feedback': feedback
    };

    // Envia una solicitud PUT a actualizar_diagnostico
    fetch(`/actualizar_diagnostico/${diagId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => response.json()).then(data => {
        if (data.status === 'success') {
            window.location.href = '/cuenta';
        } else {
            alert('There was an error submitting your feedback. Please try again later.');
            window.location.href = '/cuenta';
        }
    });
});

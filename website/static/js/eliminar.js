document.addEventListener('DOMContentLoaded', function() {
var deleteForms = document.querySelectorAll('[id^="deleteForm-"]');
    deleteForms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            var diagnosticDiv = form.closest('.result'); // Corrección: usar form.closest('.result')
            fetch(form.action, {
                method: form.method,
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: new URLSearchParams(new FormData(form)).toString()
            })
            .then(response => {
                if (response.ok) {
                    var textSymptoms = diagnosticDiv.querySelector('.data'); // Obtener el elemento textSymptoms dentro del div
textSymptoms.textContent = "ELIMINADO"; // Cambiar el contenido del elemento textSymptoms

                } else {
                    console.log('Error al eliminar el diagnóstico');
                }
            })
            .catch(error => {
                console.log('Error al eliminar el diagnóstico', error);
            });
        });
    });
});

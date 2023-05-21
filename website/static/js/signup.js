// FUNCIONES CREADAS POR JAVIER

document.querySelector('.signup').addEventListener('submit', function (e) {
    e.preventDefault();

    // Obtiene los valores del formulario
    const name = document.querySelector('#name').value;
    const surname = document.querySelector('#surname1').value;
    const surname2 = document.querySelector('#surname2').value;
    const username = document.querySelector('#username').value;
    const email = document.querySelector('#email').value;
    const password = document.querySelector('#password').value;
    const password2 = document.querySelector('#password2').value;

    console.log(name);
    console.log(surname);
    console.log(surname2);
    console.log(username);
    console.log(email);
    console.log(password);
    console.log(password2);


    // Realiza las comprobaciones de validación
    if (password !== password2) {
        alert('Las contraseñas no coinciden');
        return;
    }
    if (!/[^@]+@[^@]+\.[^@]+/.test(email)) {
        alert('El formato de correo electrónico no es válido');
        return;
    }
    if (!/[A-Za-z0-9]+/.test(username)) {
        alert('El nombre de usuario contiene caracteres no permitidos');
        return;
    }
    if (!name || !surname || !username || !email || !password || !password2) {
        alert('Todos los campos son obligatorios');
        return;
    }
    if (!/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()])([a-zA-Z\d!@#$%^&*()]{8,})$/.test(password)) {
        alert('La contraseña no cumple con los requisitos de seguridad:' + '\n' +
            'Debe contener al menos 8 caracteres' + '\n' +
            'Debe contener al menos una letra mayúscula' + '\n' +
            'Debe contener al menos una letra minúscula' + '\n' +
            'Debe contener al menos un número' + '\n' +
            'Debe contener al menos un carácter especial' + '\n' +
            'No puede contener espacios');

        return;
    }

    // Prepara los datos a enviar
    const data = {
        name: name,
        surname: surname,
        surname2: surname2,
        username: username,
        email: email,
        password: password,
    };

    // Envía los datos al servidor
    fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => {
        if (response.ok) {
            window.location.href = '/login';
        } else {
            // Si el servidor responde con un error, muestra un mensaje de alerta
            response.json().then(data => {
                alert(data.status);
            });
        }
    });
});

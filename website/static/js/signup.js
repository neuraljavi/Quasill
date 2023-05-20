document.querySelector('#signup-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const name = document.querySelector('#name').value;
    const surname = document.querySelector('#surname1').value;
    const surname2 = document.querySelector('#surname2').value;
    const username = document.querySelector('#username').value;
    const email = document.querySelector('#email').value;
    const password = document.querySelector('#password').value;

    var data = {
        'name': name,
        'surname': surname,
        'surname2': surname2,
        'username': username,
        'email': email,
        'password': password,
    };

    fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => {
        if (!response.ok) {
            return response.json().then(data => { throw new Error(data.status) })
        }
        return response.json();
    }).then(data => {
        window.location.href = '/login';
    }).catch(error => {
        alert(error);
    });
});

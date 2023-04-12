from flask import Blueprint, render_template, request, session, redirect, url_for
import re
from website.logic import login_user, register_user, update_user, delete_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            if login_user(username, password):
                print("ha entrado")
                return render_template("index.html", user=session.get('user_id'))
            else:
                print("no ha entrado")
                return redirect(url_for('auth.login'))
        except TypeError as e:
            # Handle the TypeError here, for example, by logging the error
            print("Error:", e)
            return redirect(url_for('auth.login'))
    else:
        return render_template("login.html", user=session.get('user_id'))


@auth.route('/logout')
def logout():
    session.pop('user_id')
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname1')
        surname2 = request.form.get('surname2')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        print(name, surname, surname2, username, email, password, password2)

        if password != password2:
            print("erro1")
            return redirect(url_for('auth.signup'))

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print("error2")
            return redirect(url_for('auth.signup'))

        if not re.match(r"[A-Za-z0-9]+", username):
            print("error3")
            return redirect(url_for('auth.signup'))
        if not name or not surname or not username or not email or not password or not password2:
            print("error4")
            return redirect(url_for('auth.signup'))

        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()])([a-zA-Z\d!@#$%^&*()]{8,})$", password):
            print("valida los datos")
            return redirect(url_for('auth.signup'))

        register_user(name, surname, username, email, password, surname2)
        print("usuario registrado")
        return redirect(url_for('auth.login'))
        print("jajaj error1")
    else:
        return render_template("signup.html")
    print("jajaj error2")


@auth.route('/cuenta')
def cuenta():
    return render_template("cuenta.html")


@auth.route('/editar', methods=['GET', 'POST'])
def editar():
    if request.method == 'POST':
        if request.form['submit_button'] == 'btnUpdate':
            print("Updating")
            name = request.form.get('name')
            surname = request.form.get('surname1')
            surname2 = request.form.get('surname2')
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            user_id = session.get('user_id')
            update_user(user_id, name, surname, username, email, password, surname2)
            print("usuario actualizado")
        if request.form['submit_button'] == 'btnDelete':
            print("Deleting")
            user_id = session.get('user_id')
            delete_user(user_id)
            print("usuario eliminado")
        return redirect(url_for('auth.cuenta'))
    return render_template('editar.html')

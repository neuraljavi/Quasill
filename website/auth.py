from flask import Blueprint, render_template, request, session, redirect, url_for
import re
from .logic import login_user, register_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if login_user(username, password):
            return render_template("index.html", user=session.get('user_id'))

        else:
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
        surname = request.form.get('surname')
        surname2 = request.form.get('surname2')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        print("coge los datos")
        if password != password2:
            return redirect(url_for('auth.signup'))
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return redirect(url_for('auth.signup'))
        if not re.match(r"[A-Za-z0-9]+", username):
            return redirect(url_for('auth.signup'))
        if not name or not surname or not username or not email or not password or not password2:
            return redirect(url_for('auth.signup'))
            print("error, falta algo")
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", password):
            return redirect(url_for('auth.signup'))
            print("valida los datos")
        register_user(name, surname, username, email, password, surname2)
        print("registra el usuario")
        return print("Usuario registrado") and redirect(url_for('auth.signup'))
    else:
        return render_template("signup.html")


@auth.route('/cuenta')
def cuenta():
    return render_template("cuenta.html")


@auth.route('/editar')
def editar():
    return render_template("editar.html")

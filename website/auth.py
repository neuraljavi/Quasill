from flask import Blueprint, render_template, request, session, redirect, url_for
from .logic import login_user, register_user
import re

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            return redirect(url_for('auth.login'))
        if login_user(username, password):
            return redirect(url_for('views.index'))
        else:
            return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        surname2 = request.form.get('surname2')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if password != password2:
            return redirect(url_for('auth.sign_up'))
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return redirect(url_for('auth.sign_up'))
        if not re.match(r"[A-Za-z0-9]+", username):
            return redirect(url_for('auth.sign_up'))
        if not name or not surname or not username or not email or not password or not password2:
            return redirect(url_for('auth.sign_up'))
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", password):
            return redirect(url_for('auth.sign_up'))
        register_user(name, surname, username, email, password, surname2)
        return render_template("sign_up.html", msg="User created")
    else:
        return render_template("sign_up.html")

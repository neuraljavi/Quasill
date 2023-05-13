from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
import re
from website.logic import login_user, register_user, update_user, delete_user
from website.models import User, Diagnostic
from website.logic import create_diagnostic, read_all_diagnostics, read_diagnostic, proportionate_feedback, \
    delete_diagnostic

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            if login_user(username, password):
                return render_template("index.html", user=session.get('user_id'))
            else:
                return redirect(url_for('auth.login'))
        except TypeError as e:
            print("Error:", e)
            return redirect(url_for('auth.login'))
    else:
        return render_template("login.html", user=session.get('user_id'))


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

        if password != password2:
            return redirect(url_for('auth.signup'))

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return redirect(url_for('auth.signup'))

        if not re.match(r"[A-Za-z0-9]+", username):
            return redirect(url_for('auth.signup'))
        if not name or not surname or not username or not email or not password or not password2:
            return redirect(url_for('auth.signup'))

        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()])([a-zA-Z\d!@#$%^&*()]{8,})$", password):
            return redirect(url_for('auth.signup'))

        register_user(name, surname, username, email, password, surname2)
        return redirect(url_for('auth.login'))
    else:
        return render_template("signup.html")


@auth.route('/cuenta')
def cuenta():
    return render_template("cuenta.html")


@auth.route('/editar', methods=['GET', 'POST'])
def editar():
    if request.method == 'POST':
        submit_button = request.form.get('submit_button')
        user_id = session.get('user_id')

        if submit_button == 'btnUpdate':
            name = request.form.get('name')
            surname = request.form.get('surname1')
            surname2 = request.form.get('surname2')
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')

            update_user(user_id, name, surname, username, email, password, surname2)

        elif submit_button == 'btnDelete':
            delete_user(user_id)

        return redirect(url_for('auth.cuenta'))
    return render_template('editar.html')


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views.index'))


# Crear un diagnóstico
@auth.route('/new-diagnostics', methods=['POST'])
def create_diagnostic():
    user_id = session.get('user_id')
    text = request.form.get('text')
    create_diagnostic(user_id, text)
    return jsonify({'status': 'success', 'message': 'Diagnostic created'}), 201


@auth.route('/diagnostics', methods=['GET'])
def read_all_diagnostics():
    user_id = session.get('user_id')
    diagnostics = read_all_diagnostics(user_id)
    return jsonify(diagnostics), 200


@auth.route('/diagnostics/<int:diagnostic_id>', methods=['PUT'])
def get_diagnostic_feedback(diagnostic_id):
    user_id = session.get('user_id')
    correct_label = request.get('correct_label')
    success = proportionate_feedback(user_id, diagnostic_id, correct_label)
    if success:
        return jsonify({'status': 'success', 'message': 'Diagnostic updated'}), 200
    else:
        return jsonify({'status': 'failure', 'message': 'Diagnostic not found'}), 404


# Borrar un diagnóstico
@auth.route('/diagnostics/<int:diagnostic_id>', methods=['DELETE'])
def delete_diagnostic_route(diagnostic_id):
    user_id = session.get('user_id')
    success = delete_diagnostic(user_id, diagnostic_id)
    if success:
        return jsonify({'status': 'success', 'message': 'Diagnostic deleted'}), 200
    else:
        return jsonify({'status': 'failure', 'message': 'Diagnostic not found'}), 404

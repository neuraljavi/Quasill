from flask import Blueprint, render_template, request, session, redirect, url_for
from azure.cosmos import CosmosClient
from .models import User
import os
import hashlib
import re

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


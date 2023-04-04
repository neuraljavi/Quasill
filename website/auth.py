from flask import Blueprint, render_template, request, session, redirect, url_for
from azure.cosmos import CosmosClient
from .models import User
import os
import hashlib
import re

auth = Blueprint('auth', __name__)

url = "https://quasilldemo.documents.azure.com:443/"
key = "mcNSjp5GoICXNMaynSrSMtgTGRcnQkMlVuXVAp0hf9UeVMEzpj1kY4pzGF05aSOp82NZiAgKwD95ACDb4zftIQ=="
client = CosmosClient(url, credential=key)
database = client.get_database_client("quasilldb")
container = database.get_container_client("users")


def register_user(name, surname, username, email, password, surname2=None):
    query = "SELECT max(c.id) as id FROM c"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    if len(items) == 0:
        id = 1
    else:
        id = items[0]['id'] + 1
    user = User(name, surname, username, email, user_id=id, surname2=surname2)
    salt = os.urandom(32)
    password_bytes = password.encode('utf-8')
    salt_bytes = salt
    hash_key = hashlib.pbkdf2_hmac('sha256', password_bytes, salt_bytes, 100000)
    salt_and_hash = salt_bytes + hash_key
    user.password = salt_and_hash
    container.upsert_item(user.to_dict())
    session['user_id'] = user.id


def login_user(username, password):
    query = "SELECT * FROM c WHERE c.username = @username"
    params = [dict(name="@username", value=username)]
    items = list(container.query_items(query=query, parameters=params, enable_cross_partition_query=True))
    if len(items) == 0:
        return False
    user = User(**items[0])
    salt = user.password[:32]
    password_bytes = password.encode('utf-8')
    hash_key = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, 100000)
    salt_and_hash = salt + hash_key
    if salt_and_hash == user.password:
        session['user_id'] = user.id
        return True
    else:
        return False


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
from azure.cosmos import CosmosClient
from .models import User, Diagnostic
from flask import session
import os
import hashlib

url = os.environ["url"]
key = os.environ["key"]
client = CosmosClient(url, credential=key)
database = client.get_database_client(os.environ["database"])
container = database.get_container_client(os.environ["container"])


def get_user_by_id(user_id):
    query = "SELECT * FROM c WHERE c.id = @id"
    params = [dict(name="@id", value=user_id)]
    items = list(container.query_items(query=query, parameters=params, enable_cross_partition_query=True))
    if len(items) == 0:
        return None
    return User(**items[0])


def register_user(name, surname, username, email, password, surname2=None):
    query = "SELECT VALUE MAX(c.id) FROM c"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    if not items or items[0] is None:
        id = 1
    else:
        id = int(items[0]) + 1
    print(id)
    user = User(name, surname, username, email, surname2=surname2, id=str(id))
    salt = os.urandom(32)
    password_bytes = password.encode('utf-8')
    salt_bytes = salt
    hash_key = hashlib.pbkdf2_hmac('sha256', password_bytes, salt_bytes, 100000)
    salt_hex = salt_bytes.hex()
    hash_hex = hash_key.hex()
    salt_and_hash = salt_hex + hash_hex
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
    salt_hex = user.password[:64]
    salt = bytes.fromhex(salt_hex)
    password_bytes = password.encode('utf-8')
    hash_key = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, 100000)
    hash_hex = hash_key.hex()
    if salt_hex + hash_hex == user.password:
        session['user_id'] = user.id
        return True
    else:
        return False


def delete_user(user_id):
    user = get_user_by_id(user_id)
    container.delete_item(user.id, partition_key=user.username)
    return True


def update_user(user_id, name, surname, username, email, password, surname2=None):
    user = get_user_by_id(user_id)
    user.name = name
    user.surname = surname
    user.username = username
    user.email = email
    if password:
        salt = os.urandom(32)
        password_bytes = password.encode('utf-8')
        salt_bytes = salt
        hash_key = hashlib.pbkdf2_hmac('sha256', password_bytes, salt_bytes, 100000)
        salt_and_hash = salt_bytes + hash_key
        user.password = salt_and_hash.hex()
    if surname2:
        user.surname2 = surname2
    container.upsert_item(user.to_dict())
    return True


def create_diagnostic(user_id: str, text: str, container):
    user = get_user_by_id(user_id, container)
    if user:
        diagnostic = user.diagnosticate(text)
        container.upsert_item(user.to_dict())
        return True
    return False


def read_diagnostic(user_id: str, diagnostic_index: int, container) -> Diagnostic:
    user = get_user_by_id(user_id, container)
    if user:
        return user.get_diagnostic(diagnostic_index)
    return None


def delete_diagnostic(user: User, diagnostic_index: int):
    if 0 <= diagnostic_index < len(user.diagnostics):
        user.delete_diagnostic(diagnostic_index)
        container.upsert_item(user.to_dict())
        return True
    return False


def proportionate_feedback(user: User, diagnostic_index: int, text: str, correct_label: str, container):
    if 0 <= diagnostic_index < len(user.diagnostics):
        feedback_successful = user.proportionate_feedback(diagnostic_index, text, correct_label)
        if feedback_successful:
            container.upsert_item(user.to_dict())
            return feedback_successful
    return False


def read_all_diagnostics(user_id: str, container) -> list[Diagnostic]:
    user = get_user_by_id(user_id, container)
    if user:
        return user.get_diagnostics()
    return []



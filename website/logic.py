from azure.cosmos import CosmosClient
from .models import User
from flask import session
import os
import hashlib

url = "https://quasilldemo.documents.azure.com:443/"
key = "mcNSjp5GoICXNMaynSrSMtgTGRcnQkMlVuXVAp0hf9UeVMEzpj1kY4pzGF05aSOp82NZiAgKwD95ACDb4zftIQ=="
client = CosmosClient(url, credential=key)
database = client.get_database_client("quasilldb")
container = database.get_container_client("users")


def register_user(name, surname, username, email, password, surname2=None):
    query = "SELECT VALUE MAX(c.id) as id FROM c"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    if not items or items[0] is None:
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
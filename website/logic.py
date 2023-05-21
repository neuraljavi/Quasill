from azure.cosmos.exceptions import CosmosResourceNotFoundError
from azure.core.exceptions import HttpResponseError
from azure.cosmos import exceptions, CosmosClient
from .models import User, Diagnostic
from flask import session
import os
import hashlib

url = os.environ["url"]
key = os.environ["key"]
client = CosmosClient(url, credential=key)
database = client.get_database_client(os.environ["database"])
container = database.get_container_client(os.environ["container"])
counter_container = database.get_container_client(os.environ["VERIFICATOR"])


# FUNCIONES CRUD PARA LOS USUARIOS CREADOS POR ALEJANDRA


# COGEMOS EL ID DEL USUARIO
def get_user_by_id(user_id):
    try:
        query = "SELECT * FROM c WHERE c.id = @id"
        params = [dict(name="@id", value=user_id)]
        items = list(container.query_items(query=query, parameters=params, enable_cross_partition_query=True))
        if len(items) == 0:
            return None
        return User.from_dict(items[0])
    # Asignar el error a una variable con "as"
    except exceptions.CosmosResourceNotFoundError as e:
        print(f"User with id {user_id} not found with error {e}")
        return None


# REGISTRAMOS AL USUARIO
def register_user(name, surname, username, email, password, surname2=None):
    # COMPROBAR QUE EL USERNAME O EMAIL YA EXISTEN EN LA BBDD

    query_username = f"SELECT * FROM c WHERE c.username = '{username}'"
    items_username = list(container.query_items(query=query_username, enable_cross_partition_query=True))
    query_email = f"SELECT * FROM c WHERE c.email = '{email}'"
    items_email = list(container.query_items(query=query_email, enable_cross_partition_query=True))

    if items_username or items_email:
        print('El nombre de usuario ya existe')
        print('El correo electrónico ya existe')
        return False
    else:
        # OBTENER EL VALOR ACTUAL DE ID
        query = f"SELECT * FROM c WHERE c.id = 'counter'"
        items = list(counter_container.query_items(query=query, enable_cross_partition_query=True))
        if not items or items[0] is None:
            user_id = 1
            counter = {'id': 'counter', 'value': 1}
            counter_container.upsert_item(counter)
        else:
            user_id = items[0]['value'] + 1
            items[0]['value'] = user_id
            counter_container.upsert_item(items[0])
        print(user_id)
        user = User(name, surname, username, email, surname2=surname2, id=str(user_id))
        # HASHEAMOS LA CONTRASEÑA DEL USUARIO CREADO POR JAVIER
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
        return True


# EL USUARIO PUEDE HACER LOGIN CON SU USUARIO Y CONTRASEÑA
def login_user(username, password):
    query = "SELECT * FROM c WHERE c.username = @username"
    params = [dict(name="@username", value=username)]
    items = list(container.query_items(query=query, parameters=params, enable_cross_partition_query=True))
    if len(items) == 0:
        return False
    user = User(**items[0])
    print(f"El user es: {items[0]}")
    # HASHING CREADO POR JAVIER
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


# BORRAMOS AL USUARIO

def delete_user(user_id):
    try:
        user = get_user_by_id(user_id)
        # EL VALOR DE LA PARTITION KEY ES EL ID DEL USUARIO
        container.delete_item(item=user_id, partition_key=user.id)
        print('Usuario eliminado exitosamente')
        return True
    except CosmosResourceNotFoundError:
        print('Usuario no encontrado')
        return False
    except HttpResponseError as e:
        print(f'Ha ocurrido un error al eliminar el usuario: {e}')
        return False


# EDITAMOS LOS DATOS DEL USUARIO
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
    # SI to do BIEN, ACTUALIZAMOS EL USUARIO
    container.upsert_item(user.to_dict())
    return True


# FUNCIONES CRUD PARA LOS DIAGNÓSTICOS CREADOS POR JAVIER

# CREAMOS UN DIAGNÓSTICO QUE DEVUELVA EL DIAGNÓSTICO
def create_diagnostic(user_id: str, text: str):
    user = get_user_by_id(user_id)
    if user:
        diagnostic = user.diagnosticate(text)
        container.upsert_item(user.to_dict())
        if diagnostic and 'predictions' in diagnostic.to_dict():
            predictions = diagnostic.to_dict()['predictions']
            return {
                'disease': list(predictions.keys())[0],
                'probability': list(predictions.values())[0]
            }
    return None


# LEEMOS UN DIAGNÓSTICO
def read_diagnostic(user_id: str, diagnostic_index: int):
    user = get_user_by_id(user_id)
    if user:
        diagnostic = user.get_diagnostic(diagnostic_index)
        if diagnostic and 'predictions' in diagnostic.to_dict():
            predictions = diagnostic.to_dict()['predictions']
            # Devuelve las 6 predicciones principales
            # Lista de tuplas (enfermedad, probabilidad)
            top_predictions = sorted(predictions.items(), key=lambda x: x[1], reverse=True)[:6]
            return top_predictions
    return None


# BORRAMOS UN DIAGNÓSTICO
def delete_diagnostic(user_id, diagnostic_index):
    user = get_user_by_id(user_id)
    if user:
        success = user.delete_diagnostic(diagnostic_index)
        if success:
            # ACTUALIZAMOS LA LISTA DEL USUARIO EN LA BBDD
            container.upsert_item(user.to_dict())
            return True
    return False


# PROPORCIONAMOS FEEDBACK RELACIONADO CON EL DIAGNÓSTICO
# ACTUALIZAMOS EL DIAGNÓSTICO CON EL FEEDBACK EN LA BBDD
def proportionate_feedback(user_id, diagnostic_index: int, correct_label: str):
    user = get_user_by_id(user_id)
    if 0 <= diagnostic_index < len(user.diagnostics):
        feedback_successful = user.proportionate_feedback(diagnostic_index, correct_label)
        if feedback_successful:
            try:
                container.upsert_item(user.to_dict())
                return True
            except exceptions.CosmosHttpResponseError:
                return False
            return True
    return False


# LEEMOS TODOS LOS DIAGNÓSTICOS
def read_all_diagnostics(user_id: str) -> list[Diagnostic]:
    user = get_user_by_id(user_id)
    if user:
        return user.get_diagnostics()
    return []

from flask import Flask, request, session, redirect, url_for
import os
import json


def load_variables_from_json(file_path):
    with open(file_path) as f:
        data = json.load(f)
        for key, value in data["Values"].items():
            os.environ[key] = value


def create_app():
    # CREAMOS INSTANCIA DE LA APP FLASK
    app = Flask(__name__)
    # CLAVE SECRETA PARA MANTENER SESIONES DE USUARIOS SEGURAS
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    # IMPORTAMOS LAS VISTAS Y VISTAS EN AUTH
    from .views import views
    from .auth import auth

    # BLUEPRINTS DE FLASK DEFINE RUTAS Y MANTIENE EL CÓDIGO ORDENADO
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app

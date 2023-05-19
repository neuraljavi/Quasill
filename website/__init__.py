from flask import Flask, request, session, redirect, url_for
import os
import json


def load_variables_from_json(file_path):
    with open(file_path) as f:
        data = json.load(f)
        for key, value in data["Values"].items():
            os.environ[key] = value


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app


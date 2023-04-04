from flask import Flask, request, session, redirect, url_for


def create_app():
    app = Flask(__name__)
    # encrypt cookies and session data related to a website
    app.config['SECRET_KEY'] = 'kimtaeraeblep1er'

    # import the views and auth files
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')  # the prefix will just be '/'
    app.register_blueprint(auth, url_prefix='/')

    return app

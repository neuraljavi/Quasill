from flask import Flask


def create_app():
    app = Flask(__name__)
    # encrypt cookies and session data related to a website
    app.config['SECRET_KEY'] = 'kimtaeraeblep1er'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app

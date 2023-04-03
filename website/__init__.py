from flask import Flask
from azure.cosmos import CosmosClient

url = "https://quasilldemo.documents.azure.com:443/"
key = "mcNSjp5GoICXNMaynSrSMtgTGRcnQkMlVuXVAp0hf9UeVMEzpj1kY4pzGF05aSOp82NZiAgKwD95ACDb4zftIQ=="
client = CosmosClient(url, credential=key)
database = client.get_database_client("quasilldb")
container = database.get_container_client("users")


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
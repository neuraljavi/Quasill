from flask import send_from_directory
from website import create_app, load_variables_from_json

load_variables_from_json("local.settings.json")
app = create_app()


# PARA ACCEDER A LOS ARCHIVOS DE LA CARPETA STATIC
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


# if we run this file, we will execute this line
if __name__ == "__main__":
    app.run(debug=True)

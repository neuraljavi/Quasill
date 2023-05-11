from flask import send_from_directory
from website import create_app, load_variables_from_json

app = create_app()


# so static files can be accessed
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


# if we run this file, we will execute this line
if __name__ == "__main__":
    load_variables_from_json("local.settings.json")
    app.run(debug=True)

from flask import Blueprint, render_template, session

# Blueprint is a way to organize a group of related views and other code
views = Blueprint('views', __name__)


@views.route('/')
def index():
    return render_template("index.html") \
        if not session.get('user_id') \
        else render_template("index2.html", user=session.get('user_id'))


@views.route('/index2')
def index2():
    return render_template("index2.html")


@views.route('/nosotros')
def nosotros():
    return render_template("nosotros.html") \
        if not session.get('user_id') \
        else render_template("nosotros2.html", user=session.get('user_id'))


@views.route('/enfermedad')
def enfermedad():
    return render_template("enfermedad.html")

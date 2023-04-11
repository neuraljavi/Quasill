from flask import Blueprint, render_template, session

# Blueprint is a way to organize a group of related views and other code
views = Blueprint('views', __name__)


@views.route('/')
def index():
    return render_template("index.html") if not session.get('user_id') else render_template("index.html", user=session.get('user_id'))

@views.route('/index2')
def home():
    return render_template("index2.html")

@views.route('/diagnostico')
def diagnostico():
    return render_template("diagnostico.html")


@views.route('/feedback')
def feedback():
    return render_template("feedback.html")


@views.route('/nosotros')
def nosotros():
    return render_template("nosotros.html")


@views.route('/resultados')
def resultados():
    return render_template("resultados.html")

@views.route('/enfermedad')
def enfermedad():
    return render_template("enfermedad.html")

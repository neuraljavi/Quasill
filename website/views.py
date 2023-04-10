from flask import Blueprint, render_template

# Blueprint is a way to organize a group of related views and other code
views = Blueprint('views', __name__)


@views.route('/')  # this is a decorator
def index():
    return render_template("index.html")

@views.route('/diagnosis')
def diagnosis():
    return render_template("diagnosis.html")

@views.route('/feedback')
def feedback():
    return render_template("feedback.html")

@views.route('/home')
def home():
    return render_template("home.html")

@views.route('/nosotros')
def nosotros():
    return render_template("nosotros.html")

@views.route('/results')
def results():
    return render_template("results.html")

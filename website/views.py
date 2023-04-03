from flask import Blueprint, render_template

# Blueprint is a way to organize a group of related views and other code
views = Blueprint('views', __name__)


@views.route('/')  # this is a decorator
def index():
    return render_template("index.html")



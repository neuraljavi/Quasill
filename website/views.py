from flask import Blueprint, render_template, session

# Blueprint is a way to organize a group of related views and other code
views = Blueprint('views', __name__)


@views.route('/')  # this is a decorator
def index():
    return render_template("index.html") if not session.get('user_id') else render_template("index.html", user=session.get('user_id'))



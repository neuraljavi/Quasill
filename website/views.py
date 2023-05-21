from flask import Blueprint, render_template, session

# CREAMOS UN BLUEPRINT PARA VIEWS QUE NO ESTÁN DIRECTAMENTE RELACIONADAS CON EL USUARIO
views = Blueprint('views', __name__)


# RUTAS DE VIEWS DE ALEJANDRA

# HAY 2 TEMPLATES DE INDEX Y SE MUESTRA UNA O LA OTRA SI EL USUARIO ESTÁ LOGUEADO O NO
@views.route('/')
def index():
    return render_template("index.html") \
        if not session.get('user_id') \
        else render_template("index2.html", user=session.get('user_id'))


@views.route('/index2')
def index2():
    return render_template("index2.html")


# HAY 2 TEMPLATES DE NOSOTROS Y SE MUESTRA UNA O LA OTRA SI EL USUARIO ESTÁ LOGUEADO O NO
@views.route('/nosotros')
def nosotros():
    return render_template("nosotros.html") \
        if not session.get('user_id') \
        else render_template("nosotros2.html", user=session.get('user_id'))


@views.route('/enfermedad')
def enfermedad():
    return render_template("enfermedad.html")

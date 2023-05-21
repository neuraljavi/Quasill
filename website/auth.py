from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
import re

from pyexpat import model

from diagnosticator import DISEASES, update_model
from website.logic import get_user_by_id, login_user, register_user, update_user, delete_user, create_diagnostic, \
    read_all_diagnostics, read_diagnostic, proportionate_feedback, delete_diagnostic
from website.models import Diagnostic, new_diagnostic

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            if login_user(username, password):
                print("ha entrado")
                return render_template("index2.html", user=session.get('user_id'))
            else:
                print("no ha entrado")
                return redirect(url_for('auth.login'))
        except TypeError as e:
            print("Error:", e)
            return redirect(url_for('auth.login'))
    else:
        return render_template("login.html", user=session.get('user_id'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.json
        name = data['name']
        surname = data['surname']
        surname2 = data['surname2']
        username = data['username']
        email = data['email']
        password = data['password']

        # Registra al usuario
        if register_user(name, surname, username, email, password, surname2):
            return jsonify({'status': 'Usuario registrado'}), 200
        else:
            return jsonify({'status': 'El nombre de usuario o el correo electrónico ya están en uso'}), 409
    else:
        return render_template("signup.html")



# A LA RUTA CUENTA LE PASAMOS LOS DATOS DEL USUARIO Y LOS DIAGNÓSTICOS QUE HA REALIZADO
@auth.route('/cuenta')
def cuenta():
    user = get_user_by_id(session['user_id'])
    diagnostics = user.get_diagnostics()
    return render_template("cuenta.html", user=user, diagnostics=diagnostics)


@auth.route('/editar', methods=['GET', 'POST'])
def editar():
    user_id = session.get('user_id')
    user = get_user_by_id(user_id)
    if request.method == 'POST':
        if request.form['submit_button'] == 'btnUpdate':
            name = request.form.get('name')
            surname = request.form.get('surname1')
            surname2 = request.form.get('surname2')
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            update_user(user_id, name, surname, username, email, password, surname2)
            print("Usuario actualizado")
            return redirect(url_for('auth.cuenta'))
        elif request.form['submit_button'] == 'btnDelete':
            # delete user
            delete_user(user_id)
            print("Usuario eliminado")
            return redirect(url_for('views.index'))
    return render_template('editar.html', user=user)


@auth.route('/eliminar', methods=['GET', 'POST'])
def eliminar():
    if request.method == 'POST':
        return redirect(url_for('auth.eliminar_cuenta'))
    return render_template('eliminar.html')


@auth.route('/eliminar_cuenta', methods=['POST'])
def eliminar_cuenta():
    user_id = session.get('user_id')
    print(f"usuario: {user_id}")
    if user_id:
        if delete_user(user_id):
            session.clear()
            print('Usuario eliminado exitosamente', 'success')
        else:
            print('Usuario no encontrado', 'danger')
    else:
        print('Usuario no autenticado', 'danger')
    return redirect(url_for('views.index'))


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views.index'))


# RUTAS RELACIONADAS CON EL DIAGNÓSTICO

# RUTA QUE LLEVA A DIAGNOSTICO PARA QUE EL USUARIO PUEDA INTRODUCIR SUS SÍNTOMAS
@auth.route('/diagnostico', methods=['POST', 'GET'])
# no solo POST sino también GET por si alguien quiere acceder a la URL de /diagnostico de forma directa
def diagnostico():
    if request.method == 'POST':
        text = request.form.get('inputSintomas')
        print(text)
        user_id = session.get('user_id')
        print(user_id)
        diagnostic_data = create_diagnostic(user_id, text)
        print(diagnostic_data)
        return redirect(url_for('auth.resultados'))

    else:
        return render_template('diagnostico.html', result=False)


# MOSTRAMOS LOS RESULTADOS DEL DIAGNÓSTICO
@auth.route('/resultados', methods=['GET'])
@auth.route('/resultados/<int:diag_id>', methods=['GET'])
def resultados(diag_id=None):
    user = get_user_by_id(session['user_id'])
    if user:
        diagnostics = user.diagnostics
        if diag_id is not None:
            # Obtén el diagnóstico específico si 'diag_id' está presente
            if diag_id >= 0 and diag_id < len(diagnostics):
                diagnostic_data = diagnostics[diag_id]
            else:
                return "Diagnostic not found", 404
        else:
            # De lo contrario, obtén el último diagnóstico
            diagnostic_data = user.get_last_diagnostic()

        print(diagnostic_data)
        probabilities = diagnostic_data.return_diseases()
        print(probabilities)
        sorted_probabilities = dict(sorted(probabilities.items(), key=lambda item: item[1], reverse=True))
        top_diseases = list(sorted_probabilities.items())[:6]

        return render_template('resultados.html', top_diseases=top_diseases)
    return render_template('resultados.html', top_diseases=[])



@auth.route('/mostrar_diagnosticos', methods=['GET'])
def mostrar_diagnosticos():
    user_id = session.get('user_id')
    if user_id:
        diagnostics = read_all_diagnostics(user_id)
        diagnostic_list = []
        for diagnostic in diagnostics:
            diagnostic_dict = {
                'disease': diagnostic['disease'],
                'probability': diagnostic['probability']
            }
            diagnostic_list.append(diagnostic_dict)
        return jsonify(diagnostics=diagnostic_list), 200
    return jsonify(diagnostics=[]), 200


@auth.route('/get_diagnostic/<int:diagnostic_id>', methods=['GET'])
def get_diagnostic(user_id: str, diagnostic_index: int) -> Diagnostic:
    diagnostic = read_diagnostic(user_id, diagnostic_index)
    return jsonify(diagnostic), 200


# btnsubmit
@auth.route('/actualizar_diagnostico/<int:diagnostic_id>', methods=['PUT'])
def actualizar_diagnostico(diagnostic_id):
    print("actualizando")
    user_id = session.get('user_id')
    diagnostic_id = int(diagnostic_id)
    correct_label = request.json.get('correct_label')
    success = proportionate_feedback(user_id=user_id, diagnostic_index=diagnostic_id, correct_label=correct_label)
    if success:
        return jsonify({'status': 'success', 'message': 'Diagnostic updated'}), 200
    else:
        return jsonify({'status': 'failure', 'message': 'Diagnostic not found'}), 404


@auth.route('/delete_diagnostic', methods=['POST'])
def delete_diagnostic_route():
    print("borrando")
    user_id = session.get('user_id')
    diagnostic_index = request.form.get('index')

    if diagnostic_index:
        delete_diagnostic(user_id, diagnostic_index)
        print("borrado")
    return redirect(url_for('auth.cuenta'))


@auth.route('/feedback/<diag_id>', methods=['GET', 'POST'], endpoint='feedback')
def feedback(diag_id):
    # now you can use diag_id in your function
    return render_template('feedback.html')


@auth.route('/select_diagnostic/<int:diagnostic_id>', methods=['GET'])
def select_diagnostic_route(diagnostic_id):
    return redirect(url_for('auth.resultados', diag_id=diagnostic_id))

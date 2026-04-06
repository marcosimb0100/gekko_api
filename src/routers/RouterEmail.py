from flask import Blueprint, jsonify, request, send_file
from helpers.HelperSecurity import Seguridad
from helpers.HelperEmail import EmailHelper
from helpers.HelperFile import enviarArchivo
from os import path

main = Blueprint('email_blueprint', __name__)


@main.route('/', methods=['POST'])
def post_put():
    has_access = Seguridad.verificar_token(request.headers)
    if not has_access['status'] == 200:
        return jsonify(has_access['data']), has_access['status']
    try:
        datos = request.get_json()
        resultado = EmailHelper.crear_actualizar( request.id_usuario, datos )
        return jsonify(resultado['data']), resultado['status']
    except Exception as ex:
        return jsonify({'mensaje': str(ex), 'datos': {}}), 500
    
    
@main.route('/', methods=['GET'])
def get():
    has_access = Seguridad.verificar_token(request.headers)
    if not has_access['status'] == 200:
        return jsonify(has_access['data']), has_access['status']
    try:
        resultado = EmailHelper.servidor_correo_electronico()
        return jsonify(resultado['data']), resultado['status']
    except Exception as ex:
        return jsonify({'mensaje': str(ex), 'datos': {}}), 500


@main.route('/probar/<correo>', methods=['GET'])
def get_probar(correo):
    has_access = Seguridad.verificar_token(request.headers)
    if not has_access['status'] == 200:
        return jsonify(has_access['data']), has_access['status']
    try:
        resultado = EmailHelper.probar_correo(correo)
        return jsonify(resultado['data']), resultado['status']
    except Exception as ex:
        return jsonify({'mensaje': str(ex), 'datos': {}}), 500

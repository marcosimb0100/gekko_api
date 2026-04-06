from flask import Blueprint, jsonify, request, send_file
from helpers.HelperSecurity import Seguridad
from helpers.HelperFile import enviarArchivo
from helpers.HelperCompany import CompanyHelper
from os import path

main = Blueprint('companias_blueprint', __name__)


@main.route('/', methods=['POST'])
def post_compania():
    has_access = Seguridad.verificar_token(request.headers)
    if not has_access['status'] == 200:
        return jsonify(has_access['data']), has_access['status']
    try:
        datos = request.get_json()
        resultado = CompanyHelper.crear( request.id_usuario, datos )
        return jsonify(resultado['data']), resultado['status']
    except Exception as ex:
            return jsonify({'mensaje': str(ex), 'datos': {}}), 500


@main.route('/', methods=['PUT'])
def put_compania():
    has_access = Seguridad.verificar_token(request.headers)
    if not has_access['status'] == 200:
        return jsonify(has_access['data']), has_access['status']
    try:
        datos = request.get_json()
        resultado = CompanyHelper.actualizar( request.id_usuario, datos )
        return jsonify(resultado['data']), resultado['status']
    except Exception as ex:
            return jsonify({'mensaje': str(ex), 'datos': {}}), 500


@main.route('/', methods=['GET'])
def get_companias():
    has_access = Seguridad.verificar_token(request.headers)
    if not has_access['status'] == 200:
        return jsonify(has_access['data']), has_access['status']
    try:
        resultado = CompanyHelper.companias()
        return jsonify(resultado['data']), resultado['status']
    except Exception as ex:
            return jsonify({'mensaje': str(ex), 'datos': {}}), 500
       

@main.route('/logo/<rfc>', methods=['POST'])
def post_logo(rfc):
    has_access = Seguridad.verificar_token(request.headers)
    if not has_access['status'] == 200:
        return jsonify(has_access['data']), has_access['status']
    try:
        print('aca')
        resultado = CompanyHelper.guardar_logo_compania( request.id_usuario, rfc, request.files )
        return jsonify(resultado['data']), resultado['status']
    except Exception as ex:
        return jsonify({'mensaje': str(ex), 'datos': {}}), 500
    
    
@main.route('/logo/<rfc>', methods=['PUT'])
def put_logo(rfc):
    has_access = Seguridad.verificar_token(request.headers)
    if not has_access['status'] == 200:
        return jsonify(has_access['data']), has_access['status']
    try:
        print('aca')
        resultado = CompanyHelper.actualizar_logo_compania( request.id_usuario, rfc, request.files )
        return jsonify(resultado['data']), resultado['status']
    except Exception as ex:
        return jsonify({'mensaje': str(ex), 'datos': {}}), 500
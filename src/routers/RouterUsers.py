from flask import Blueprint, jsonify, request, send_file
from helpers.HelperSecurity import Seguridad
from helpers.HelperUsers import UsuarioHelper
from helpers.HelperFile import enviarArchivo
from os import path

main = Blueprint('usuarios_blueprint', __name__)


@main.route('/', methods=['POST'])
def post_usuario():
    # has_access = Seguridad.verificar_token(request.headers)
    # if not has_access['status'] == 200:
    #     return jsonify(has_access['data']), has_access['status']
    try:
        datos = request.get_json()
        resultado = UsuarioHelper.crear( datos )
        return jsonify(resultado['data']), resultado['status']
    except Exception as ex:
            return jsonify({'mensaje': str(ex), 'datos': {}}), 500
        
        
@main.route('/', methods=['PUT'])
def put_usuario():
#     has_access = Seguridad.verificar_token(request.headers)
#     if not has_access['status'] == 200:
#         return jsonify(has_access['data']), has_access['status']
    try:
        datos = request.get_json()
        resultado = UsuarioHelper.actualizar(datos)  
        return jsonify(resultado['data']), resultado['status']
    except Exception as ex:
        return jsonify({'mensaje': str(ex), 'datos': {}}), 500
    
    
@main.route('/usuario', methods=['GET'])
def get_usuarios_usuario():
    has_access = Seguridad.verificar_token(request.headers)
    if not has_access['status'] == 200:
        return jsonify(has_access['data']), has_access['status']
    try:
        return jsonify({ 'mensaje': 'Consulta exitosa!.', 'datos': { 'correo_electronico': request.correo_electronico, 'nombre_completo': request.nombre_completo } }), 200
    except Exception as ex:
        return jsonify({'mensaje': str(ex), 'datos': {}}), 500


@main.route('/acceso', methods=['POST'])
def post_usuario_acceso():
    try:
        datos = request.get_json()
        resultado = UsuarioHelper.acceso( datos )
        return jsonify(resultado['data']), resultado['status']
    except Exception as ex:
            return jsonify({'mensaje': str(ex), 'datos': {}}), 500
        
        
        
@main.route('/foto', methods=['PUT'])
def put_foto():
    has_access = Seguridad.verificar_token(request.headers)
    if not has_access['status'] == 200:
        return jsonify(has_access['data']), has_access['status']
    try:
        resultado = UsuarioHelper.guardar_foto_perfil( request.id_usuario, request.files )
        return jsonify(resultado['data']), resultado['status']
    except Exception as ex:
        return jsonify({'mensaje': str(ex), 'datos': {}}), 500
    
    
    
@main.route('/foto', methods=['GET'])
def get_foto():
    has_access = Seguridad.verificar_token(request.headers)
    if not has_access['status'] == 200:
        return jsonify(has_access['data']), has_access['status']
    try:
        resultado = UsuarioHelper.mostrar_foto_perfil(request.id_usuario)
        route = enviarArchivo( f"\\upload\\profiles\\{resultado}" )
        if path.isfile( route ):
            return send_file( route )
        else:
            route = enviarArchivo( f"\\files\\profile_photos\\perfil.png" )
            return send_file( route )
    except Exception as ex:
        return jsonify({'mensaje': str(ex), 'datos': {}}), 500
    
    

@main.route('/foto/<id>', methods=['GET'])
def get_foto_id(id):
    has_access = Seguridad.verificar_token(request.headers)
    if not has_access['status'] == 200:
        return jsonify(has_access['data']), has_access['status']
    try:
        resultado = UsuarioHelper.mostrar_foto_perfil(id)
        route = enviarArchivo( f"\\upload\\profiles\\{resultado}" )
        if path.isfile( route ):
            return send_file( route )
        else:
            route = enviarArchivo( f"\\files\\profile_photos\\perfil.png" )
            return send_file( route )
    except Exception as ex:
        return jsonify({'mensaje': str(ex), 'datos': {}}), 500
    
    
    
    
@main.route('/usuarios', methods=['GET'])
def get_usuarios():
    has_access = Seguridad.verificar_token(request.headers)
    if not has_access['status'] == 200:
        return jsonify(has_access['data']), has_access['status']
    try:
        resultado = UsuarioHelper.usuarios()
        return jsonify(resultado['data']), resultado['status']
    except Exception as ex:
        return jsonify({'mensaje': str(ex), 'datos': {}}), 500
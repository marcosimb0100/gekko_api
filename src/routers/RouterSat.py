from flask import Blueprint, jsonify, request, send_file
from helpers.HelperSecurity import Seguridad
from helpers.HelperSat import SatHelper

main = Blueprint('sat_blueprint', __name__)

@main.route('/sat_empresa', methods=['GET'])
def get_sat_empresa():
    has_access = Seguridad.verificar_token(request.headers)
    if not has_access['status'] == 200:
        return jsonify(has_access['data']), has_access['status']
    try:
        resultado = SatHelper.catalogos_empresa()
        return jsonify(resultado['data']), resultado['status']
    except Exception as ex:
        return jsonify({'mensaje': str(ex), 'datos': {}}), 500
    
    
@main.route('/sat_productos_servicios/<dato>', methods=['GET'])
def sat_productos_servicios(dato):
    has_access = Seguridad.verificar_token(request.headers)
    if not has_access['status'] == 200:
        return jsonify(has_access['data']), has_access['status']
    try:
        resultado = SatHelper.catalogos_filtro_producto_servicio(dato)
        return jsonify(resultado['data']), resultado['status']
    except Exception as ex:
        return jsonify({'mensaje': str(ex), 'datos': {}}), 500

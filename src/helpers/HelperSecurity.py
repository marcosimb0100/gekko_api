from flask import request, jsonify, g
from config import current_config
from bson import ObjectId
from dataBase.mongo import cnn_mongo
import datetime
import jwt
import pytz
import json
import shortuuid


class Seguridad():
    
    
    secret      = current_config.JWT
    tz          = pytz.timezone("America/Mexico_City")
    
    
    @classmethod
    def generar_token(cls, datos):
        
        payload={
            'iat': datetime.datetime.now( tz = cls.tz ),
            'exp': datetime.datetime.now( tz = cls.tz ) + datetime.timedelta( hours = int(current_config.JWT_HRS) ),
            'id': str(datos.get("_id")) if datos.get("_id") else None
        }
        
        
        UUID                                = shortuuid.ShortUUID().random(length=10)
        db                                  = cnn_mongo()
        ahora                               = datetime.datetime.now(cls.tz) 
        return jwt.encode(payload, cls.secret, algorithm="HS256")
    
    
    @classmethod
    def verificar_token(cls, headers):
        try:
            if 'Authorization' in headers.keys():
                token = headers['Authorization']
                rutaActual = headers['rutaActual']
                encoded_token = token.split(" ")[1]
                if(len(encoded_token) > 0):
                    try:
                        payload                             = jwt.decode( encoded_token, cls.secret, algorithms=["HS256"] )
                        db                                  = cnn_mongo()
                        usuario                             = db["usuarios"].find_one( { "_id": ObjectId(payload['id']), "activo": True } )
                        if not usuario:
                            return { 'status': 401, "data": { 'mensaje': 'El usuario no es valido!', 'datos': {} } }
                        
                        setattr(request, "id_usuario", payload['id'])
                        setattr(request, "correo_electronico", usuario['correo_electronico'])
                        setattr(request, "nombre_completo", usuario['nombre_completo'])
                        
                        g.correo_electronico = usuario['correo_electronico']
                        g.nombre_completo = usuario['nombre_completo']
                        
                        # db                                  = cnn_mongo()
                        # perfil                              = db["perfilesUsuarios"].find_one({ "id_usuario": request.id_usuario })
                        # perfilMenu                          = db["perfiles"].find_one({ "id_perfil": perfil['id_perfil'] })
                        # arrayUrl                            = json.loads(perfilMenu['lista_url'])
                        # if not (rutaActual in arrayUrl):
                        #     return { 'status': 403, "data": { 'mensaje': 'Sin acceso a la ruta.', 'datos': {} } }
                        
                        return { 'status': 200, "data": { 'mensaje': '', 'datos': {} } }
                    except jwt.ExpiredSignatureError:
                        return { 'status': 401, "data": { 'mensaje': 'El token a expirado!', 'datos': {} } }
                    except jwt.InvalidTokenError:
                        return { 'status': 401, "data": { 'mensaje': 'Token no valido!', 'datos': {} } }
            else:
                return { 'status': 401, "data": { 'mensaje': 'Este EndPoint requiere de un token para ser utilizado!', 'datos': {} } }
        except Exception as ex:
            return { 'status': 401, "data": { 'mensaje': str(ex), 'datos': {} } }
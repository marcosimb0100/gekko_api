from dataBase.mongo import cnn_mongo
from models.ModelUsers import UsuarioModel
from helpers.HelperSecurity import Seguridad
from helpers.HelperFile import archivoRuta
from datetime import datetime
from bson import ObjectId
import bcrypt
import shortuuid

from models.ModelUsers import UsuarioModel

class UsuarioHelper():
    
    @classmethod
    def crear(self, datos):
        try:
            
            fecha_actual                        = datetime.now()
            sal                                 = bcrypt.gensalt()
            clave                               = datos['clave']
            clave_hashed                        = bcrypt.hashpw(clave.encode('utf-8'), sal)
            clave_hashed_str                    = clave_hashed.decode('utf-8')
            db                                  = cnn_mongo()
            
            if db["usuarios"].find_one({"correo_electronico": datos['correo_electronico'].lower()}):
                return { 'status': 400, "data": { 'mensaje': 'El correo electrónico ya existe.', 'datos': {} } }
            
            usuario = UsuarioModel(

                correo_electronico      = datos['correo_electronico'].lower(),
                nombre_completo         = datos['nombre_completo'].upper(),
                clave                   = clave_hashed_str,
                foto_perfil             = "perfil.png",
                
                activo                  = True,
                fecha_creacion          = fecha_actual
            )
            respDB = db["usuarios"].insert_one(usuario.dict(by_alias=True))
            
            if respDB.inserted_id:
                resultado = { 'status': 200, "data": { 'mensaje': 'Inserción correcta!', 'datos': {} } }
            else:
                resultado = { 'status': 400, "data": { 'mensaje': 'La inserción falló.', 'datos': {} } }
            
            return resultado
        except Exception as ex:
            return { 'status': 500, "data": { 'mensaje': str(ex), 'datos': {} } }
        
        
    @classmethod
    def actualizar(self, datos):
        try:

            fecha_actualizacion                 = datetime.now()
            db                                  = cnn_mongo()
            usuario_actualizado = {
                
                "correo_electronico": datos['correo_electronico'].lower(), 
                "nombre_completo": datos['nombre_completo'].upper(), 
                
                "activo": self.str_to_bool(datos['activo']),
                
                "fecha_actualizacion": fecha_actualizacion,
                "fecha_inactivo": fecha_actualizacion if not self.str_to_bool(datos['activo']) else None
                
            }
            respDB = db["usuarios"].update_one(
                { "id_usuario": datos['id_usuario'] },  
                { "$set": usuario_actualizado }
            )
            
            if respDB.modified_count > 0:
                resultado = { 'status': 200, "data": { 'mensaje': 'Actualización correcta!', 'datos': {} } }
            else:
                resultado = { 'status': 400, "data": { 'mensaje': 'La actualización falló.', 'datos': {} } }
            
            return resultado
        except Exception as ex:
            return { 'status': 500, "data": { 'mensaje': str(ex), 'datos': {} } }
        
        
        
    @classmethod
    def clave(self, datos):
        try:
            
            fecha_actualizacion                 = datetime.now()
            db                                  = cnn_mongo()
            sal                                 = bcrypt.gensalt()
            clave                               = datos['clave']
            clave_hashed                        = bcrypt.hashpw(clave.encode('utf-8'), sal)
            clave_hashed_str                    = clave_hashed.decode('utf-8')
            
            usuario_actualizado = {
                "clave": clave_hashed_str,
                "fecha_actualizacion": fecha_actualizacion
            }
            respDB = db["usuarios"].update_one(
                { "id_usuario": datos['id_usuario'] },  
                { "$set": usuario_actualizado }
            )
            
            if respDB.modified_count > 0:
                resultado = { 'status': 200, "data": { 'mensaje': 'Actualización correcta!', 'datos': {} } }
            else:
                resultado = { 'status': 400, "data": { 'mensaje': 'La actualización falló.', 'datos': {} } }
            
            return resultado
        except Exception as ex:
            return { 'status': 500, "data": { 'mensaje': str(ex), 'datos': {} } }
        
        
    @classmethod
    def usuarios(self):
        try:
            
            db                                  = cnn_mongo()
            usuarios                            = list(db["usuarios"].find({}, {"clave": 0}))

            usuarios_serializados = []
            for usuario in usuarios:
                usuario_serializado = {
                    
                    "_id": str(usuario.get("_id")) if usuario.get("_id") else None,
                    "correo_electronico": usuario.get("correo_electronico"),
                    "nombre_completo": usuario.get("nombre_completo"),

                    "activo": usuario.get("activo"),

                    "fecha_creacion": usuario.get("fecha_creacion"),
                    "fecha_actualizacion": usuario.get("fecha_actualizacion"),
                    "fecha_inactivo": usuario.get("fecha_inactivo")
                }

                if isinstance(usuario_serializado["fecha_creacion"], datetime):
                    usuario_serializado["fecha_creacion"] = usuario_serializado["fecha_creacion"].isoformat()
                    
                if isinstance(usuario_serializado["fecha_actualizacion"], datetime):
                    usuario_serializado["fecha_actualizacion"] = usuario_serializado["fecha_actualizacion"].isoformat()
                    
                if isinstance(usuario_serializado["fecha_inactivo"], datetime):
                    usuario_serializado["fecha_inactivo"] = usuario_serializado["fecha_inactivo"].isoformat()

                usuarios_serializados.append(usuario_serializado)
            
            resultado = { 'status': 200, "data": { 'mensaje': 'Consulta correcta!', 'datos': { "usuarios": usuarios_serializados } } }
            
            return resultado
        except Exception as ex:
            return { 'status': 500, "data": { 'mensaje': str(ex), 'datos': {} } }
        
        
    @classmethod
    def acceso(self, datos):
        try:
            db                                  = cnn_mongo()
            usuario                             = db["usuarios"].find_one( { "correo_electronico": datos['correo_electronico'], "activo": True } )
            if not usuario:
                return { 'status': 400, "data": { 'mensaje': 'El correo electronico no existe o el usuario esta dado de baja!', 'datos': {} } }
            
            hash_almacenado                     = bytes( usuario["clave"], encoding='utf-8' )
            rest                                = bcrypt.checkpw( datos['clave'].encode('utf-8'), hash_almacenado )
            if not rest:
                return { 'status': 400, "data": { 'mensaje': 'La clave es incorrecta!', 'datos': {} } }
            
            token                               = Seguridad.generar_token( usuario )
            resultado = { 'status': 200, "data": { 'mensaje': 'Acceso correcto!', 'datos': { "token": ( f"Bearer {token}" ), "nombre_completo": usuario['nombre_completo'], "correo_electronico": usuario['correo_electronico']  } } }
            return resultado
        
        except Exception as ex:
            print(ex)
            return str(ex)
        

    @classmethod
    def guardar_foto_perfil(self, id, imagen):
        try:
            
            fecha_actualizacion                 = datetime.now()
            db                                  = cnn_mongo()
            ruta, archivoFoto                   = archivoRuta( "\\upload\\profiles\\", imagen['foto_perfil'], id )
            usuario_actualizado = {
                "foto_perfil": f"{archivoFoto}",
                "fecha_actualizacion": fecha_actualizacion
            }
            respDB = db["usuarios"].update_one(
                { "_id": ObjectId(id) },
                { "$set": usuario_actualizado }
            )
            if respDB.modified_count > 0:
                imagen['foto_perfil'].save( ruta )
                resultado = { 'status': 200, "data": { 'mensaje': 'Actualización correcta!', 'datos': {} } }
            else:
                resultado = { 'status': 400, "data": { 'mensaje': 'La actualización falló.', 'datos': {} } }
            
            return resultado
        except Exception as ex:
            print(str(ex))
            return { 'status': 500, "data": { 'mensaje': str(ex), 'datos': {} } }


    @classmethod
    def mostrar_foto_perfil(self, id):
        try:
            db                                  = cnn_mongo()
            usuario_foto_perfil                 = db["usuarios"].find_one({ "_id": ObjectId(id) })
            return usuario_foto_perfil['foto_perfil']
        except Exception as ex:
            return str(ex)
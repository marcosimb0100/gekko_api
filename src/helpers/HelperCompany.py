from dataBase.mongo import cnn_mongo
from models.ModelCompany import CompanyModel, BankCompanyModel
from helpers.HelperSecurity import Seguridad
from helpers.HelperFile import archivoRuta
from datetime import datetime
from bson import ObjectId
import bcrypt


class CompanyHelper():
    
    @staticmethod
    def formatear_diccionario(datos):
        return {
            k.replace('_', ' ').title(): v
            for k, v in datos.items()
            if k != '_id'
        }
    
    
    @staticmethod
    def serialize_datetime(value):
        return value.isoformat() if isinstance(value, datetime) else value
    
        
    @classmethod
    def crear(cls, idUsuario, datos):
        try:

            fecha_actual                        = datetime.now()
            db                                  = cnn_mongo()
            
            if db["companias"].find_one({"rfc": datos['rfc'].upper()}):
                return { 'status': 400, "data": { 'mensaje': 'El R.F.C. ya existe.', 'datos': {} } }
            
            compania = CompanyModel(

                logo                            = "perfil.png",
                
                tipo_persona                    = datos['tipo_persona'].lower(),
                rfc                             = datos['rfc'].upper(),
                razon_social_nombre_completo    = datos['razon_social_nombre_completo'].upper(),
                
                calle                           = datos['calle'].upper(),
                numero_ext                      = datos['numero_ext'].upper(),
                numero_int                      = datos['numero_int'].upper(),
                colonia                         = datos['colonia'].upper(),
                poblacion                       = datos['poblacion'].upper(),
                municipio                       = datos['municipio'].upper(),
                codigo_postal                   = datos['codigo_postal'].upper(),
                
                pais                            = datos['pais'].upper(),
                estado                          = datos['estado'].upper(),
                
                correo_electronico              = datos['correo_electronico'].lower(),
                numero_contacto_principal       = datos['numero_contacto_principal'].upper(),
                numero_contacto_alterno         = datos['numero_contacto_alterno'].upper(),
                
                regimen_fiscal                  = datos['regimen_fiscal'].upper(),
                
                representante_legal             = "",
                
                id_usuario_creo                 = idUsuario,
                
                activo                          = datos['activo'],
                
                fecha_creacion                  = fecha_actual,
                fecha_inactivo                  = fecha_actual if not datos['activo'] else None
                
            )
            respDB = db["companias"].insert_one(compania.dict(by_alias=True))
            
            if respDB.inserted_id:
                
                company_id = respDB.inserted_id

                bancos = datos.get("bancos", [])
                bancos_insertados = []

                for banco_item in bancos:
                    banco = BankCompanyModel(
                        company_id=company_id,
                        clabe_banco=(banco_item.get("clabe_banco") or "").upper(),
                        banco=(banco_item.get("banco") or "").upper(),
                        cuenta_banco=(banco_item.get("cuenta_banco") or "").upper(),
                        id_usuario_creo=idUsuario,
                        activo=banco_item.get("activo", True),
                        fecha_creacion=fecha_actual,
                        fecha_inactivo=fecha_actual if not banco_item.get("activo", True) else None
                    )

                    resp_banco = db["companias_bancos"].insert_one(banco.dict(by_alias=True))
                    bancos_insertados.append(str(resp_banco.inserted_id))

                
                resultado = { 'status': 200, "data": { 'mensaje': 'Inserción correcta!', 'datos': {} } }
            else:
                resultado = { 'status': 400, "data": { 'mensaje': 'La inserción falló.', 'datos': {} } }
            
            return resultado
        except Exception as ex:
            return { 'status': 500, "data": { 'mensaje': str(ex), 'datos': {} } }


    @classmethod
    def actualizar(cls, idUsuario, datos):
        try:
            fecha_actual = datetime.now()
            db = cnn_mongo()

            company_id = datos.get("_id")
            if not company_id:
                return {
                    "status": 400,
                    "data": {
                        "mensaje": "El _id de la compañía es requerido.",
                        "datos": {}
                    }
                }

            company_id = ObjectId(company_id)

            compania_existente = db["companias"].find_one({"_id": company_id})
            if not compania_existente:
                return {
                    "status": 404,
                    "data": {
                        "mensaje": "La compañía no existe.",
                        "datos": {}
                    }
                }

            compania_rfc = db["companias"].find_one({
                "rfc": datos.get("rfc"),
                "_id": {"$ne": company_id}
            })
            if compania_rfc:
                return {
                    "status": 400,
                    "data": {
                        "mensaje": "El R.F.C. ya existe en otra compañía.",
                        "datos": {}
                    }
                }

            update_compania = {
                "tipo_persona":                     (datos.get("tipo_persona") or "").lower(),
                "rfc":                              (datos.get("rfc")).upper(),
                "razon_social_nombre_completo":     (datos.get("razon_social_nombre_completo") or "").upper(),

                "calle":                            (datos.get("calle") or "").upper(),
                "numero_ext":                       (datos.get("numero_ext") or "").upper(),
                "numero_int":                       (datos.get("numero_int") or "").upper(),
                "colonia":                          (datos.get("colonia") or "").upper(),
                "poblacion":                        (datos.get("poblacion") or "").upper(),
                "municipio":                        (datos.get("municipio") or "").upper(),
                "codigo_postal":                    (datos.get("codigo_postal") or "").upper(),

                "pais":                             (datos.get("pais") or "").upper(),
                "estado":                           (datos.get("estado") or "").upper(),

                "correo_electronico":               (datos.get("correo_electronico") or "").lower(),
                "numero_contacto_principal":        datos.get("numero_contacto_principal"),
                "numero_contacto_alterno":          datos.get("numero_contacto_alterno"),

                "regimen_fiscal":                   datos.get("regimen_fiscal"),
                "representante_legal":              "",

                "id_usuario_modifico":              idUsuario,
                
                "activo":                           datos.get("activo"),
                "fecha_actualizacion":              fecha_actual,
                "fecha_inactivo":                   fecha_actual if not datos.get("activo", True) else None
            }

            db["companias"].update_one(
                {"_id": company_id},
                {"$set": update_compania}
            )

            bancos = datos.get("bancos", [])
            bancos_actualizados = []
            bancos_insertados = []

            for banco_item in bancos:
                banco_id = banco_item.get("_id")

                update_banco = {
                    "company_id":                   company_id,
                    "clabe_banco":                  (banco_item.get("clabe_banco") or "").upper(),
                    "banco":                        (banco_item.get("banco") or "").upper(),
                    "cuenta_banco":                 (banco_item.get("cuenta_banco") or "").upper(),
                    "id_usuario_modifico":          idUsuario,
                    "activo":                       banco_item.get("activo"),
                    "fecha_actualizacion":          fecha_actual,
                    "fecha_inactivo":               fecha_actual if not banco_item.get("activo", True) else None
                }

                if banco_id:
                    db["companias_bancos"].update_one(
                        {
                            "_id": ObjectId(banco_id),
                            "company_id": company_id
                        },
                        {"$set": update_banco}
                    )
                    bancos_actualizados.append(banco_id)
                else:
                    nuevo_banco = {
                        "company_id":               company_id,
                        "clabe_banco":              (banco_item.get("clabe_banco") or "").upper(),
                        "banco":                    (banco_item.get("banco") or "").upper(),
                        "cuenta_banco":             (banco_item.get("cuenta_banco") or "").upper(),
                        "id_usuario_creo":          idUsuario,
                        "activo":                   banco_item.get("activo"),
                        "fecha_creacion":           fecha_actual,
                        "fecha_inactivo":           fecha_actual if not banco_item.get("activo", True) else None
                    }

                    resp_banco = db["companias_bancos"].insert_one(nuevo_banco)
                    bancos_insertados.append(str(resp_banco.inserted_id))

            return {
                "status": 200,
                "data": {
                    "mensaje": "Actualización correcta.",
                    "datos": {
                        "company_id": str(company_id),
                        "bancos_actualizados": bancos_actualizados,
                        "bancos_insertados": bancos_insertados
                    }
                }
            }

        except Exception as ex:
            return {
                "status": 500,
                "data": {
                    "mensaje": str(ex),
                    "datos": {}
                }
            }


    @classmethod
    def companias(cls):
        try:
            db = cnn_mongo()

            pipeline = [
                {
                    "$lookup": {
                        "from": "companias_bancos",
                        "localField": "_id",
                        "foreignField": "company_id",
                        "as": "bancos"
                    }
                },
                {
                    "$project": {
                        "tipo_persona": 1,
                        "rfc": 1,
                        "razon_social_nombre_completo": 1,

                        "calle": 1,
                        "numero_ext": 1,
                        "numero_int": 1,
                        "colonia": 1,
                        "poblacion": 1,
                        "municipio": 1,
                        "codigo_postal": 1,

                        "pais": 1,
                        "estado": 1,

                        "correo_electronico": 1,
                        "numero_contacto_principal": 1,
                        "numero_contacto_alterno": 1,

                        "regimen_fiscal": 1,
                        "representante_legal": 1,

                        "id_usuario_creo": 1,
                        "id_usuario_modifico": 1,

                        "activo": 1,
                        "fecha_creacion": 1,
                        "fecha_actualizacion": 1,
                        "fecha_inactivo": 1,

                        "bancos": 1
                    }
                }
            ]

            companias = list(db["companias"].aggregate(pipeline))

            companias_serializados = [
                {
                    "_id":                              str(compania["_id"]) if compania.get("_id") else None,

                    "tipo_persona":                     compania.get("tipo_persona"),
                    "rfc":                              compania.get("rfc"),
                    "razon_social_nombre_completo":     compania.get("razon_social_nombre_completo"),

                    "calle":                            compania.get("calle"),
                    "numero_ext":                       compania.get("numero_ext"),
                    "numero_int":                       compania.get("numero_int"),
                    "colonia":                          compania.get("colonia"),
                    "poblacion":                        compania.get("poblacion"),
                    "municipio":                        compania.get("municipio"),
                    "codigo_postal":                    compania.get("codigo_postal"),

                    "pais":                             compania.get("pais"),
                    "estado":                           compania.get("estado"),

                    "correo_electronico":               compania.get("correo_electronico"),
                    "numero_contacto_principal":        compania.get("numero_contacto_principal"),
                    "numero_contacto_alterno":          compania.get("numero_contacto_alterno"),

                    "regimen_fiscal":                   compania.get("regimen_fiscal"),
                    "representante_legal":              compania.get("representante_legal"),

                    "id_usuario_creo":                  str(compania.get("id_usuario_creo")) if compania.get("id_usuario_creo") else None,
                    "id_usuario_modifico":              str(compania.get("id_usuario_modifico")) if compania.get("id_usuario_modifico") else None,

                    "activo":                           compania.get("activo"),

                    "fecha_creacion":                   CompanyHelper.serialize_datetime(compania.get("fecha_creacion")),
                    "fecha_actualizacion":              CompanyHelper.serialize_datetime(compania.get("fecha_actualizacion")),
                    "fecha_inactivo":                   CompanyHelper.serialize_datetime(compania.get("fecha_inactivo")),

                    "bancos": [
                        {
                            "_id":                      str(banco["_id"]) if banco.get("_id") else None,
                            "company_id":               str(banco.get("company_id")) if banco.get("company_id") else None,
                            "clabe_banco":              banco.get("clabe_banco"),
                            "banco":                    banco.get("banco"),
                            "cuenta_banco":             banco.get("cuenta_banco"),
                            "id_usuario_creo":          str(banco.get("id_usuario_creo")) if banco.get("id_usuario_creo") else None,
                            "id_usuario_modifico":      str(banco.get("id_usuario_modifico")) if banco.get("id_usuario_modifico") else None,
                            "activo":                   banco.get("activo"),
                            "fecha_creacion":           CompanyHelper.serialize_datetime(banco.get("fecha_creacion")),
                            "fecha_actualizacion":      CompanyHelper.serialize_datetime(banco.get("fecha_actualizacion")),
                            "fecha_inactivo":           CompanyHelper.serialize_datetime(banco.get("fecha_inactivo")),
                        }
                        for banco in compania.get("bancos", [])
                    ]
                }
                for compania in companias
            ]

            return {
                "status": 200,
                "data": {
                    "mensaje": "Consulta correcta!",
                    "datos": {
                        "companias": companias_serializados
                    }
                }
            }

        except Exception as ex:
            return {
                "status": 500,
                "data": {
                    "mensaje": str(ex),
                    "datos": {}
                }
            }


    @classmethod
    def guardar_logo_compania(self, idUsuario, rfc, imagen):
        try:
            
            fecha_actualizacion                 = datetime.now()
            db                                  = cnn_mongo()
            ruta, archivoFoto                   = archivoRuta( f"\\upload\\companies\\{rfc}\\", imagen['logo'], rfc )
            compania_actualizado = {
                "logo": f"{archivoFoto}",
                "id_usuario_modifico": idUsuario,
                "fecha_actualizacion": fecha_actualizacion
            }
            respDB = db["companias"].update_one(
                { "rfc": (rfc).upper() },
                { "$set": compania_actualizado }
            )
            if respDB.modified_count > 0:
                imagen['logo'].save( ruta )
                resultado = { 'status': 200, "data": { 'mensaje': 'Logo guardado.', 'datos': {} } }
            else:
                resultado = { 'status': 400, "data": { 'mensaje': 'Fallo el guardado del logo.', 'datos': {} } }
            
            return resultado
        except Exception as ex:
            print(str(ex))
            return { 'status': 500, "data": { 'mensaje': str(ex), 'datos': {} } }


    @classmethod
    def actualizar_logo_compania(self, idUsuario, rfc, imagen):
        try:
            
            fecha_actualizacion                 = datetime.now()
            db                                  = cnn_mongo()
            ruta, archivoFoto                   = archivoRuta( f"\\upload\\companies\\{rfc}\\", imagen['logo'], rfc )
            compania_actualizado = {
                "logo": f"{archivoFoto}",
                "id_usuario_modifico": idUsuario,
                "fecha_actualizacion": fecha_actualizacion
            }
            respDB = db["companias"].update_one(
                { "rfc": (rfc).upper() },
                { "$set": compania_actualizado }
            )
            if respDB.modified_count > 0:
                imagen['logo'].save( ruta )
                resultado = { 'status': 200, "data": { 'mensaje': 'Logo actualizado', 'datos': {} } }
            else:
                resultado = { 'status': 400, "data": { 'mensaje': 'Fallo la actualizacion del logo.', 'datos': {} } }
            
            return resultado
        except Exception as ex:
            print(str(ex))
            return { 'status': 500, "data": { 'mensaje': str(ex), 'datos': {} } }


    @classmethod
    def logo_compania(self, id):
        try:
            db                                  = cnn_mongo()
            logo_compania                       = db["companias"].find_one({ "_id": ObjectId(id) })
            return logo_compania
        except Exception as ex:
            return str(ex)
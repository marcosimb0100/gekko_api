from dataBase.mongo import cnn_mongo
from models.ModelEmail import EmailModel
from helpers.HelperSecurity import Seguridad
from helpers.HelperFile import archivoRuta
from flask import Flask
from flask_mail import Mail, Message
from datetime import datetime
from bson import ObjectId
import bcrypt
import shortuuid
import os


class EmailHelper():
    
    @staticmethod
    def formatear_diccionario(datos):
        return {
            k.replace('_', ' ').title(): v
            for k, v in datos.items()
            if k != '_id'
        }
        

    @classmethod
    def crear_actualizar(self, idUsuario, datos):
        try:
            fecha_actualizacion = datetime.now()
            db = cnn_mongo()
            collection = db["servidor_correo_electronico"]

            correo_electronico = {
                "correo_electronico": str(datos['correo_electronico']),
                "clave": str(datos['clave']),
                "servidor_entrante": str(datos['servidor_entrante']),
                "puerto_imap": str(datos['puerto_imap']),
                "puerto_pop3": str(datos['puerto_pop3']),
                "servidor_saliente": str(datos['servidor_saliente']),
                "puerto_smtp": str(datos['puerto_smtp']),
                "id_usuario_modifico": idUsuario,
                "activo": datos['activo'],
                "fecha_actualizacion": fecha_actualizacion,
                "fecha_inactivo": fecha_actualizacion if not datos['activo'] else None
            }

            existente = collection.find_one()

            if existente:
                respDB = collection.update_one(
                    {"_id": existente["_id"]},
                    {
                        "$set": correo_electronico
                    }
                )

                if respDB.modified_count > 0 or respDB.matched_count > 0:
                    resultado = { "status": 200, "data": { "mensaje": "Actualización correcta.", "datos": {"_id": str(existente["_id"])} } }
                else:
                    resultado = { "status": 400, "data": { "mensaje": "No se pudo actualizar el registro.", "datos": {} } }

            else:
                nuevo_documento = {
                    **correo_electronico,
                    "fecha_creacion": fecha_actualizacion,
                    "id_usuario_creo": idUsuario
                }

                respDB = collection.insert_one(nuevo_documento)

                resultado = { "status": 200, "data": { "mensaje": "Registro creado correctamente.", "datos": {"_id": str(respDB.inserted_id)} } }

            return resultado

        except Exception as ex:
            return { "status": 500, "data": { "mensaje": str(ex), "datos": {} } }
        
        
    @classmethod
    def servidor_correo_electronico(self):
        try:
            
            db                                  = cnn_mongo()
            servidor_correo_electronico         = db["servidor_correo_electronico"].find_one()
            
            if not servidor_correo_electronico:
                return { 'status': 400, "data": { 'mensaje': 'No existe configuración de correo.', 'datos': {} } }
            
            data = servidor_correo_electronico

            servidor_serializado = {
                "_id": str(data.get("_id")) if data.get("_id") else None,
                "correo_electronico": data.get("correo_electronico"),
                "clave": data.get("clave"),
                "servidor_entrante": data.get("servidor_entrante"),
                "puerto_imap": data.get("puerto_imap"),
                "puerto_pop3": data.get("puerto_pop3"),
                "servidor_saliente": data.get("servidor_saliente"),
                "puerto_smtp": data.get("puerto_smtp"),
                "activo": data.get("activo"),
                "fecha_creacion": data.get("fecha_creacion"),
                "fecha_actualizacion": data.get("fecha_actualizacion"),
                "fecha_inactivo": data.get("fecha_inactivo")
            }
            
            for campo in ["fecha_creacion", "fecha_actualizacion", "fecha_inactivo"]:
                if isinstance(servidor_serializado[campo], datetime):
                    servidor_serializado[campo] = servidor_serializado[campo].isoformat()
            
            resultado = { 'status': 200, "data": { 'mensaje': 'Consulta correcta!', 'datos': { "servidor_correo_electronico": servidor_serializado } } }
            
            return resultado
        except Exception as ex:
            return { 'status': 500, "data": { 'mensaje': str(ex), 'datos': {} } }
        
    
    @classmethod
    def probar_correo(self, correo):
        
        db                                  = cnn_mongo()
        servidor_correo_electronico         = db["servidor_correo_electronico"].find_one()
        
        if not servidor_correo_electronico:
                return { 'status': 400, "data": { 'mensaje': 'No existe configuración de correo.', 'datos': {} } }
            
        app = Flask(__name__)

        app.config.update({
            'MAIL_SERVER': servidor_correo_electronico['servidor_saliente'],
            'MAIL_PORT': int(servidor_correo_electronico['puerto_smtp']),
            'MAIL_USE_SSL': True,
            'MAIL_USE_TLS': False,
            'MAIL_USERNAME': servidor_correo_electronico['correo_electronico'],
            'MAIL_PASSWORD': servidor_correo_electronico['clave'],
            'MAIL_DEFAULT_SENDER': servidor_correo_electronico['correo_electronico']
        })
        
        mail = Mail(app)
        
        try:
            with app.app_context():
                msg = Message(
                    subject="Correo de prueba Ballfudr",
                    recipients=[correo]
                )

                msg.html = """
                <html>
                    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 20px;">
                        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4;">
                            <tr>
                                <td align="center">
                                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden;">
                                        
                                        <tr>
                                            <td style="background-color:#1f4e78; padding:20px; text-align:center;">
                                                <img src="cid:logo_empresa" alt="Logo" style="max-width:190px; height:auto; display:block; margin:0 auto;">
                                            </td>
                                        </tr>
                                        
                                        <tr>
                                            <td style="background-color: #1f4e78; color: white; padding: 20px; text-align: center;">
                                                <h1 style="margin: 0;">Correo de prueba</h1>
                                            </td>
                                        </tr>

                                        <tr>
                                            <td style="padding: 30px; color: #333333;">
                                                <p style="font-size: 16px;">Hola,</p>

                                                <p style="font-size: 15px; line-height: 1.6;">
                                                    Este es un <strong>correo de prueba</strong> enviado desde
                                                    <span style="color: #1f4e78;">Ballfudr</span>.
                                                </p>


                                                <p style="font-size: 14px; color: #777777;">
                                                    Saludos,<br>
                                                    Sistema de Notificaciones
                                                </p>
                                            </td>
                                        </tr>

                                        <tr>
                                            <td style="background-color: #eeeeee; text-align: center; padding: 15px; font-size: 12px; color: #666666;">
                                                Este correo fue generado automáticamente.
                                            </td>
                                        </tr>

                                    </table>
                                </td>
                            </tr>
                        </table>
                    </body>
                </html>
                """
                
                ruta_logo = os.path.join("src", "upload", "imagenes", "logo_letra_blanco.png")

                with open(ruta_logo, "rb") as f:
                    msg.attach(
                        filename="logo_letra_blanco.png",
                        content_type="image/png",
                        data=f.read(),
                        headers={
                            "Content-ID": "<logo_empresa>",
                            "Content-Disposition": "inline; filename=logo_letra_blanco.png"
                        }
                    )

                mail.send(msg)

            return { 'status': 200, "data": { 'mensaje': 'Correo enviado correctamente', 'datos': {} } }

        except Exception as e:
            return { 'status': 500, "data": { 'mensaje': f'Error al enviar correo: {str(e)}', 'datos': {} } }
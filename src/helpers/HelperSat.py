from dataBase.mongo import cnn_mongo
from models.ModelSat import ( SatPaisModel, SatEstadoModel, SatRegimenFiscalModel, SatTipoPersonaModel, SatBancoModel, SatProductosServiciosModel )

class SatHelper:

    @classmethod
    def catalogos_empresa(self):
        try:
            db = cnn_mongo()

            sat_estado                          = list(db["sat_estado"].find({}, {"_id": 0}))
            sat_pais                            = list(db["sat_pais"].find({}, {"_id": 0}))
            sat_tipo_persona                    = list(db["sat_tipo_persona"].find({}, {"_id": 0}))
            sat_regimen_fiscal                  = list(db["sat_regimen_fiscal"].find({}, {"_id": 0}))
            sat_banco                           = list(db["sat_banco"].find({}, {"_id": 0}))

            estados                             = [SatEstadoModel(**estado).model_dump() for estado in sat_estado]
            paises                              = [SatPaisModel(**pais).model_dump() for pais in sat_pais]
            tipos_persona                       = [SatTipoPersonaModel(**tipo).model_dump() for tipo in sat_tipo_persona]
            regimenes                           = [SatRegimenFiscalModel(**regimen).model_dump() for regimen in sat_regimen_fiscal]
            bancos                              = [SatBancoModel(**banco).model_dump() for banco in sat_banco]

            resultado                           = {
                                                    "status": 200,
                                                    "data": {
                                                        "mensaje": "Consulta correcta!",
                                                        "datos": {
                                                            "tipo_persona": tipos_persona,
                                                            "pais": paises,
                                                            "estado": estados,
                                                            "regimen_fiscal": regimenes,
                                                            "banco": bancos
                                                        }
                                                    }
                                                }

            return resultado

        except Exception as ex:
            return { "status": 500, "data": { "mensaje": str(ex), "datos": {} } }
        
        
        
    @classmethod
    def catalogos_filtro_producto_servicio(cls, dato):
        try:
            db = cnn_mongo()

            filtro = {}

            if dato:
                                                filtro = {
                                                    "$or": [
                                                        {"clave_prod_serv": {"$regex": dato, "$options": "i"}},
                                                        {"descripcion": {"$regex": dato, "$options": "i"}}
                                                    ]
                                                }

            sat_prod_serv                       = list(
                                                    db["sat_prod_serv"].find(filtro, {"_id": 0}).limit(50)
                                                )

            prod_serv = []
            for item in sat_prod_serv:
                producto = SatProductosServiciosModel(**item).model_dump()
                producto["descripcion_mostrar"] = f'{producto["clave_prod_serv"]} - {producto["descripcion"]}'
                prod_serv.append(producto)
                
            print(prod_serv)

            resultado = {
                "status": 200,
                "data": {
                    "mensaje": "Consulta correcta!",
                    "datos": {
                        "prod_serv": prod_serv
                    }
                }
            }

            return resultado

        except Exception as ex:
            return {
                "status": 500,
                "data": {"mensaje": str(ex), "datos": {}}
            }
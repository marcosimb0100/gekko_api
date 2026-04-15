from dataBase.mongo import cnn_mongo
from models.ModelSat import ( SatPaisModel, SatEstadoModel, SatRegimenFiscalModel, SatTipoPersonaModel, SatBancoModel, SatProductosServiciosModel, SatClavesUnidadesModel, SatExportacionModel, SatObjetoImpModel )

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
            sat_clave_unidad                    = list(db["sat_clave_unidad"].find({}, {"_id": 0}))
            sat_exportacion                     = list(db["sat_exportacion"].find({}, {"_id": 0}))
            sat_objeto_imp                      = list(db["sat_objeto_imp"].find({}, {"_id": 0}))

            estados                             = [SatEstadoModel(**item).model_dump() for item in sat_estado]
            paises                              = [SatPaisModel(**item).model_dump() for item in sat_pais]
            tipos_persona                       = [SatTipoPersonaModel(**item).model_dump() for item in sat_tipo_persona]
            regimenes                           = [SatRegimenFiscalModel(**item).model_dump() for item in sat_regimen_fiscal]
            bancos                              = [SatBancoModel(**item).model_dump() for item in sat_banco]
            clave_unidad                        = [SatClavesUnidadesModel(**item).model_dump() for item in sat_clave_unidad]
            exportacion                         = [SatExportacionModel(**exportacion).model_dump() for exportacion in sat_exportacion]
            objeto_imp                          = [SatObjetoImpModel(**objeto_imp).model_dump() for objeto_imp in sat_objeto_imp]

            clave_unidad = [
                {
                    **SatClavesUnidadesModel(**item).model_dump(),
                    "descripcion_2": f"{item.get('clave_unidad', '')} - {item.get('descripcion', '')}"
                }
                for item in sat_clave_unidad
            ]


            exportacion = [
                {
                    **SatExportacionModel(**item).model_dump(),
                    "descripcion_2": f"{item.get('exportacion', '')} - {item.get('descripcion', '')}"
                }
                for item in sat_exportacion
            ]


            objeto_imp = [
                {
                    **SatObjetoImpModel(**item).model_dump(),
                    "descripcion_2": f"{item.get('objeto_imp', '')} - {item.get('descripcion', '')}"
                }
                for item in sat_objeto_imp
            ]


            resultado                           = {
                                                    "status": 200,
                                                    "data": {
                                                        "mensaje": "Consulta correcta!",
                                                        "datos": {
                                                            "estado": estados,
                                                            "pais": paises,
                                                            "tipo_persona": tipos_persona,
                                                            "regimen_fiscal": regimenes,
                                                            "banco": bancos,
                                                            "clave_unidad": clave_unidad,
                                                            "exportacion": exportacion,
                                                            "objeto_imp": objeto_imp
                                                        }
                                                    }
                                                }

            return resultado

        except Exception as ex:
            print( str(ex) )
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
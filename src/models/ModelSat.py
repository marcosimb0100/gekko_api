from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional, Dict, Any
from datetime import datetime


class SatEstadoModel(BaseModel):

    estado: str
    pais: str
    nombre_estado: str

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True


class SatPaisModel(BaseModel):

    pais: str
    descripcion: str

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True


class SatRegimenFiscalModel(BaseModel):

    regimen_fiscal: str
    descripcion: str
    fisica: bool
    moral: bool

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True


class SatTipoPersonaModel(BaseModel):

    tipo_persona: str
    descripcion: str

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True


class SatBancoModel(BaseModel):

    clabe_banco: str
    descripcion: str
    razon_social: str
    json_mismo_banco_nomina: Dict[str, Any]
    json_mismo_banco_transferencia: Dict[str, Any]
    json_interbancario_nomina: Dict[str, Any]
    json_interbancario_transferencia: Dict[str, Any]
    json_mismoBanco_nom_alta_cuenta: Dict[str, Any]
    json_mismoBanco_trans_alta_cuenta: Dict[str, Any]
    json_interbancario_nom_alta_cuenta: Dict[str, Any]
    json_interbancario_trans_alta_cuenta: Dict[str, Any]
    json_banorte_alta_cuenta_ar: Dict[str, Any]
    json_banorte_alta_cuenta_ac: Dict[str, Any]
    json_estado_cuenta_principal: Dict[str, Any]
    json_estado_cuenta_secundario: Dict[str, Any]
    json_estado_cuenta_alternativo: Dict[str, Any]

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True


class SatProductosServiciosModel(BaseModel):

    tipo_clave_prod_serv: str
    tipo: str
    clave_prod_serv: str
    descripcion: str    

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
# // Company

from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from datetime import datetime

class EmpresasRPModel(BaseModel):

    razon_social: Optional[str] = None
    rfc: Optional[str] = None
    siglas: Optional[str] = None
    nombre_corto: Optional[str] = None
    calle: Optional[str] = None
    numExt: Optional[str] = None
    numInt: Optional[str] = None
    colonia: Optional[str] = None
    poblacion: Optional[str] = None
    municipio: Optional[str] = None
    estado: Optional[str] = None
    pais: Optional[str] = None
    codigo_postal: Optional[str] = None
    telefono1: Optional[str] = None
    telefono2: Optional[str] = None
    representante_legal: Optional[str] = None
    
    id_usuario_creo: Optional[int] = None
    id_usuario_modifico: Optional[int] = None
    
    activo: bool = True

    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_actualizacion: Optional[datetime] = None
    fecha_inactivo: Optional[datetime] = None

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
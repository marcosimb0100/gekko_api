# // Company

from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from datetime import datetime

class CompanyModel(BaseModel):

    logo: Optional[str] = None
    
    tipo_persona: Optional[str] = None
    rfc: Optional[str] = None
    razon_social_nombre_completo: Optional[str] = None
    
    
    calle: Optional[str] = None
    numero_ext: Optional[str] = None
    numero_int: Optional[str] = None
    colonia: Optional[str] = None
    poblacion: Optional[str] = None
    municipio: Optional[str] = None
    codigo_postal: Optional[str] = None
    
    pais: Optional[str] = None
    estado: Optional[str] = None
    
    correo_electronico: Optional[str] = None
    numero_contacto_principal: Optional[str] = None
    numero_contacto_alterno: Optional[str] = None
    
    regimen_fiscal: Optional[str] = None
    
    representante_legal: Optional[str] = None
    
    id_usuario_creo: Optional[str] = None
    id_usuario_modifico: Optional[str] = None
    
    activo: bool = True

    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_actualizacion: Optional[datetime] = None
    fecha_inactivo: Optional[datetime] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        populate_by_name = True
        
        
class BankCompanyModel(BaseModel):

    company_id: Optional[ObjectId]
    
    clabe_banco: Optional[str] = None
    banco: Optional[str] = None
    cuenta_banco: Optional[str] = None
    
    id_usuario_creo: Optional[str] = None
    id_usuario_modifico: Optional[str] = None
    
    activo: bool = True

    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_actualizacion: Optional[datetime] = None
    fecha_inactivo: Optional[datetime] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        populate_by_name = True
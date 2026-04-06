from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from datetime import datetime


class EmailModel(BaseModel):

    correo_electronico: str
    clave: str
    servidor_entrante: str
    puerto_imap: str
    puerto_pop3: str
    servidor_saliente: str
    puerto_smtp: str

    id_usuario_creo: Optional[str] = None
    id_usuario_modifico: Optional[str] = None
    
    activo: bool = True

    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_actualizacion: Optional[datetime] = None
    fecha_inactivo: Optional[datetime] = None

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True

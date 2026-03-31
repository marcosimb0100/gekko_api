from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from datetime import datetime


class PerfiloModel(BaseModel):

    nombre_perfil: str
    
    menus_seleccionados: str
    menu_web: str
    
    lista_url: str
    
    empresas_seleccionados: str
    clientes_seleccionados: str

    id_usuario_creo: Optional[int] = None
    id_usuario_modifico: Optional[int] = None
    
    activo: bool = True

    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_actualizacion: Optional[datetime] = None
    fecha_inactivo: Optional[datetime] = None

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True

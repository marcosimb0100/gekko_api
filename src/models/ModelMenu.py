from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from datetime import datetime


class MenuWebModel(BaseModel):

    menu_hijo: str
    menu_padre: Optional[str] = None

    tipo_menu: str

    orden_n1: int
    orden_n2: int

    etiqueta: str
    icono: Optional[str] = None
    url: Optional[str] = None

    activo: bool = True

    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_actualizacion: Optional[datetime] = None
    fecha_inactivo: Optional[datetime] = None

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
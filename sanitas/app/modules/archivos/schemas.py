from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ArchivoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    paciente_id: int
    subido_por: Optional[int]
    nombre_archivo: str
    tipo_mime: str
    tamano: int
    descripcion: Optional[str]
    creado_en: datetime

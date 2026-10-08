from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.modules.usuarios.schemas import UsuarioResponse


class PacienteBase(BaseModel):
    fecha_nacimiento: Optional[date] = None
    dpi: Optional[str] = Field(None, max_length=30)
    telefono: Optional[str] = Field(None, max_length=30)
    tipo_sangre: Optional[str] = Field(None, max_length=10)


class PacienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    apellido: Optional[str] = Field(None, min_length=2, max_length=100)
    telefono: Optional[str] = Field(None, max_length=30)
    fecha_nacimiento: Optional[date] = None
    tipo_sangre: Optional[str] = Field(None, max_length=10)
    dpi: Optional[str] = Field(None, max_length=30)


class PacienteResponse(PacienteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    usuario: UsuarioResponse

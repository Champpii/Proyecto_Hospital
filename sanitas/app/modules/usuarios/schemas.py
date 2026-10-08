from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.modules.usuarios.models import RolUsuario


class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido: str = Field(..., min_length=2, max_length=100)
    correo: EmailStr


class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=6, max_length=100)
    rol: Optional[RolUsuario] = RolUsuario.PACIENTE


class MedicoCreate(UsuarioBase):
    password: str = Field(..., min_length=6, max_length=100)


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    apellido: Optional[str] = Field(None, min_length=2, max_length=100)
    correo: Optional[EmailStr] = None
    activo: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=6, max_length=100)


class UsuarioResponse(UsuarioBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    rol: str
    activo: bool
    creado_en: datetime

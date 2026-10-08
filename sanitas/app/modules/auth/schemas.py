from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class LoginRequest(BaseModel):
    correo: EmailStr
    password: str = Field(..., min_length=1)


class RegistroPacienteRequest(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido: str = Field(..., min_length=2, max_length=100)
    correo: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    fecha_nacimiento: Optional[date] = None
    dpi: Optional[str] = Field(None, max_length=30)
    telefono: Optional[str] = Field(None, max_length=30)
    tipo_sangre: Optional[str] = Field(None, max_length=10)


class AuthUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    apellido: str
    correo: str
    rol: str

from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.modules.antecedentes.personales.models import CategoriaPersonal


class AntecedentePersonalBase(BaseModel):
    categoria: CategoriaPersonal
    descripcion: str = Field(..., min_length=2, max_length=255)
    fecha: Optional[date] = None
    observaciones: Optional[str] = None


class AntecedentePersonalCreate(AntecedentePersonalBase):
    paciente_id: int


class AntecedentePersonalUpdate(BaseModel):
    categoria: Optional[CategoriaPersonal] = None
    descripcion: Optional[str] = Field(None, min_length=2, max_length=255)
    fecha: Optional[date] = None
    observaciones: Optional[str] = None


class AntecedentePersonalResponse(AntecedentePersonalBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    paciente_id: int
    registrado_por: Optional[int]
    categoria: str

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.modules.antecedentes.familiares.models import EstadoEnfermedadFamiliar


class AntecedenteFamiliarBase(BaseModel):
    parentesco: str = Field(..., min_length=2, max_length=50)
    enfermedad: str = Field(..., min_length=2, max_length=255)
    estado: EstadoEnfermedadFamiliar = EstadoEnfermedadFamiliar.ACTUAL
    observaciones: Optional[str] = None


class AntecedenteFamiliarCreate(AntecedenteFamiliarBase):
    paciente_id: int


class AntecedenteFamiliarUpdate(BaseModel):
    parentesco: Optional[str] = Field(None, min_length=2, max_length=50)
    enfermedad: Optional[str] = Field(None, min_length=2, max_length=255)
    estado: Optional[EstadoEnfermedadFamiliar] = None
    observaciones: Optional[str] = None


class AntecedenteFamiliarResponse(AntecedenteFamiliarBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    paciente_id: int
    registrado_por: Optional[int]
    estado: str

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies.auth import get_current_user
from app.modules.antecedentes.familiares.schemas import (
    AntecedenteFamiliarCreate,
    AntecedenteFamiliarUpdate,
    AntecedenteFamiliarResponse
)
from app.modules.antecedentes.familiares.service import AntecedenteFamiliarService
from app.modules.usuarios.models import Usuario

router = APIRouter(prefix="/familiares", tags=["Antecedentes Familiares"])


@router.post("/", response_model=AntecedenteFamiliarResponse, status_code=status.HTTP_201_CREATED)
def registrar_antecedente_familiar(
    data: AntecedenteFamiliarCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    service = AntecedenteFamiliarService(db)
    return service.registrar(data, current_user)


@router.get("/paciente/{paciente_id}", response_model=List[AntecedenteFamiliarResponse])
def listar_por_paciente(
    paciente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    service = AntecedenteFamiliarService(db)
    return service.listar_por_paciente(paciente_id, current_user)


@router.put("/{ant_id}", response_model=AntecedenteFamiliarResponse)
def actualizar_antecedente_familiar(
    ant_id: int,
    data: AntecedenteFamiliarUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    service = AntecedenteFamiliarService(db)
    return service.actualizar(ant_id, data, current_user)


@router.delete("/{ant_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_antecedente_familiar(
    ant_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    service = AntecedenteFamiliarService(db)
    service.eliminar(ant_id, current_user)
    return None

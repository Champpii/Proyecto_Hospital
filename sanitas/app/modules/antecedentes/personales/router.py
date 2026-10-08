from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies.auth import get_current_user
from app.modules.antecedentes.personales.schemas import (
    AntecedentePersonalCreate,
    AntecedentePersonalUpdate,
    AntecedentePersonalResponse
)
from app.modules.antecedentes.personales.service import AntecedentePersonalService
from app.modules.usuarios.models import Usuario

router = APIRouter(prefix="/personales", tags=["Antecedentes Personales"])


@router.post("/", response_model=AntecedentePersonalResponse, status_code=status.HTTP_201_CREATED)
def registrar_antecedente_personal(
    data: AntecedentePersonalCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    service = AntecedentePersonalService(db)
    return service.registrar(data, current_user)


@router.get("/paciente/{paciente_id}", response_model=List[AntecedentePersonalResponse])
def listar_por_paciente(
    paciente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    service = AntecedentePersonalService(db)
    return service.listar_por_paciente(paciente_id, current_user)


@router.put("/{ant_id}", response_model=AntecedentePersonalResponse)
def actualizar_antecedente_personal(
    ant_id: int,
    data: AntecedentePersonalUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    service = AntecedentePersonalService(db)
    return service.actualizar(ant_id, data, current_user)


@router.delete("/{ant_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_antecedente_personal(
    ant_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    service = AntecedentePersonalService(db)
    service.eliminar(ant_id, current_user)
    return None

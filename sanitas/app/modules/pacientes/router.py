from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies.auth import get_current_user
from app.core.dependencies.roles import require_medico_or_admin
from app.modules.pacientes.schemas import PacienteResponse, PacienteUpdate
from app.modules.pacientes.service import PacienteService
from app.modules.usuarios.models import Usuario, RolUsuario
from app.core.exceptions import ForbiddenError

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


@router.get("/", response_model=List[PacienteResponse])
def listar_pacientes(
    q: Optional[str] = Query(None, description="Búsqueda por nombre, apellido, correo o DPI"),
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_medico_or_admin)
):
    service = PacienteService(db)
    return service.listar_o_buscar(q)


@router.get("/mi-perfil", response_model=PacienteResponse)
def obtener_mi_perfil(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    service = PacienteService(db)
    return service.obtener_por_usuario(current_user.id)


@router.get("/{paciente_id}", response_model=PacienteResponse)
def obtener_paciente(
    paciente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    service = PacienteService(db)
    paciente = service.obtener_por_id(paciente_id)
    if (
        current_user.rol == RolUsuario.PACIENTE.value
        and paciente.usuario_id != current_user.id
    ):
        raise ForbiddenError("Solo puede consultar su propio historial.")
    return paciente


@router.put("/{paciente_id}", response_model=PacienteResponse)
def actualizar_paciente(
    paciente_id: int,
    data: PacienteUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    service = PacienteService(db)
    return service.actualizar_datos(paciente_id, data, current_user)

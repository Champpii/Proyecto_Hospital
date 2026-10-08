from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies.roles import require_admin
from app.modules.usuarios.schemas import UsuarioResponse, MedicoCreate, UsuarioUpdate
from app.modules.usuarios.service import UsuarioService
from app.modules.usuarios.models import Usuario

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin)
):
    service = UsuarioService(db)
    return service.listar_usuarios()


@router.post("/medicos", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_medico(
    data: MedicoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin)
):
    service = UsuarioService(db)
    return service.crear_medico(data)


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(
    usuario_id: int,
    data: UsuarioUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin)
):
    service = UsuarioService(db)
    return service.actualizar_usuario(usuario_id, data)


@router.patch("/{usuario_id}/estado", response_model=UsuarioResponse)
def cambiar_estado(
    usuario_id: int,
    activo: bool,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin)
):
    service = UsuarioService(db)
    return service.cambiar_estado(usuario_id, activo)

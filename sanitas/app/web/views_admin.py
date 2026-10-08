from pathlib import Path
from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies.roles import require_admin
from app.modules.usuarios.service import UsuarioService
from app.modules.usuarios.schemas import MedicoCreate
from app.modules.usuarios.models import Usuario, RolUsuario
from app.modules.pacientes.models import Paciente
from app.core.exceptions import AppException

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
router = APIRouter(prefix="/admin", tags=["Web Administrador"])


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_admin(
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_admin)
):
    service = UsuarioService(db)
    todos = service.listar_usuarios()
    total_pacientes = db.query(Paciente).count()
    total_medicos = sum(1 for u in todos if u.rol == RolUsuario.MEDICO.value and u.activo)
    total_admins = sum(1 for u in todos if u.rol == RolUsuario.ADMINISTRADOR.value)

    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard.html",
        context={
            "usuario_actual": usuario,
            "total_usuarios": len(todos),
            "total_pacientes": total_pacientes,
            "total_medicos": total_medicos,
            "total_admins": total_admins,
        }
    )


@router.get("/usuarios", response_class=HTMLResponse)
def admin_usuarios_page(
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_admin)
):
    service = UsuarioService(db)
    usuarios = service.listar_usuarios()
    return templates.TemplateResponse(
        request=request,
        name="admin/usuarios.html",
        context={"usuario_actual": usuario, "usuarios": usuarios}
    )


@router.post("/usuarios/medico")
def crear_medico_web(
    request: Request,
    nombre: str = Form(...),
    apellido: str = Form(...),
    correo: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_admin)
):
    service = UsuarioService(db)
    try:
        dto = MedicoCreate(
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            password=password
        )
        service.crear_medico(dto)
        return RedirectResponse(url="/admin/usuarios", status_code=status.HTTP_303_SEE_OTHER)
    except AppException as e:
        usuarios = service.listar_usuarios()
        return templates.TemplateResponse(
            request=request,
            name="admin/usuarios.html",
            context={
                "usuario_actual": usuario,
                "usuarios": usuarios,
                "error": e.message
            },
            status_code=400
        )


@router.post("/usuarios/{usuario_id}/toggle-estado")
def toggle_usuario_estado(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_admin)
):
    service = UsuarioService(db)
    target = service.obtener_por_id(usuario_id)
    if target.id != usuario.id:
        service.cambiar_estado(usuario_id, not target.activo)
    return RedirectResponse(url="/admin/usuarios", status_code=status.HTTP_303_SEE_OTHER)

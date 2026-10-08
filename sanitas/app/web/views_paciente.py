from datetime import date
from typing import Optional
from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies.auth import get_current_user
from app.core.dependencies.roles import require_paciente
from app.modules.pacientes.service import PacienteService
from app.modules.pacientes.schemas import PacienteUpdate
from pathlib import Path
from app.modules.usuarios.models import Usuario
from app.core.exceptions import AppException

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
router = APIRouter(prefix="/paciente", tags=["Web Paciente"])


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_paciente(
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_paciente)
):
    service = PacienteService(db)
    paciente = service.obtener_por_usuario(usuario.id)
    return templates.TemplateResponse(
        request=request,
        name="paciente/dashboard.html",
        context={"usuario_actual": usuario, "paciente": paciente}
    )


@router.get("/perfil", response_class=HTMLResponse)
def perfil_paciente(
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_paciente)
):
    service = PacienteService(db)
    paciente = service.obtener_por_usuario(usuario.id)
    return templates.TemplateResponse(
        request=request,
        name="paciente/perfil.html",
        context={"usuario_actual": usuario, "paciente": paciente}
    )


@router.post("/perfil")
def actualizar_perfil_paciente(
    request: Request,
    nombre: str = Form(...),
    apellido: str = Form(...),
    dpi: Optional[str] = Form(None),
    telefono: Optional[str] = Form(None),
    fecha_nacimiento: Optional[str] = Form(None),
    tipo_sangre: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_paciente)
):
    service = PacienteService(db)
    paciente = service.obtener_por_usuario(usuario.id)
    try:
        f_nac = date.fromisoformat(fecha_nacimiento) if fecha_nacimiento else None
        update_dto = PacienteUpdate(
            nombre=nombre,
            apellido=apellido,
            dpi=dpi,
            telefono=telefono,
            fecha_nacimiento=f_nac,
            tipo_sangre=tipo_sangre
        )
        service.actualizar_datos(paciente.id, update_dto, usuario)
        return RedirectResponse(url="/paciente/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    except AppException as e:
        return templates.TemplateResponse(
            request=request,
            name="paciente/perfil.html",
            context={"usuario_actual": usuario, "paciente": paciente, "error": e.message},
            status_code=400
        )

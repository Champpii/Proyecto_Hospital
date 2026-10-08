from datetime import date
from typing import Optional
from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.core.security.session import create_session_token
from app.core.dependencies.auth import get_current_user_optional
from app.modules.auth.schemas import LoginRequest, RegistroPacienteRequest
from app.modules.auth.service import AuthService
from pathlib import Path
from app.modules.usuarios.models import Usuario, RolUsuario
from app.core.exceptions import AppException

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
router = APIRouter(tags=["Web Auth"])


@router.get("/", response_class=HTMLResponse)
def index_redirect(usuario: Optional[Usuario] = Depends(get_current_user_optional)):
    if not usuario:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    if usuario.rol == RolUsuario.PACIENTE.value:
        return RedirectResponse(url="/paciente/dashboard", status_code=status.HTTP_302_FOUND)
    elif usuario.rol == RolUsuario.MEDICO.value:
        return RedirectResponse(url="/medico/dashboard", status_code=status.HTTP_302_FOUND)
    return RedirectResponse(url="/admin/dashboard", status_code=status.HTTP_302_FOUND)


@router.get("/login", response_class=HTMLResponse)
def pagina_login(request: Request, usuario: Optional[Usuario] = Depends(get_current_user_optional)):
    if usuario:
        return index_redirect(usuario)
    return templates.TemplateResponse(
        request=request,
        name="auth/login.html",
        context={"usuario_actual": None}
    )


@router.post("/auth/web/login")
def procesar_login_web(
    request: Request,
    correo: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    service = AuthService(db)
    try:
        usuario = service.autenticar(LoginRequest(correo=correo, password=password))
        token = create_session_token(usuario.id)
        redirect_url = "/"
        if usuario.rol == RolUsuario.PACIENTE.value:
            redirect_url = "/paciente/dashboard"
        elif usuario.rol == RolUsuario.MEDICO.value:
            redirect_url = "/medico/dashboard"
        elif usuario.rol == RolUsuario.ADMINISTRADOR.value:
            redirect_url = "/admin/dashboard"

        resp = RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)
        resp.set_cookie(
            key=settings.SESSION_COOKIE_NAME,
            value=token,
            httponly=True,
            max_age=86400,
            samesite="lax"
        )
        return resp
    except AppException as e:
        return templates.TemplateResponse(
            request=request,
            name="auth/login.html",
            context={"error": e.message, "usuario_actual": None},
            status_code=400
        )


@router.get("/registro", response_class=HTMLResponse)
def pagina_registro(request: Request, usuario: Optional[Usuario] = Depends(get_current_user_optional)):
    if usuario:
        return index_redirect(usuario)
    return templates.TemplateResponse(
        request=request,
        name="auth/registro.html",
        context={"usuario_actual": None}
    )


@router.post("/auth/web/registro")
def procesar_registro_web(
    request: Request,
    nombre: str = Form(...),
    apellido: str = Form(...),
    correo: str = Form(...),
    password: str = Form(...),
    fecha_nacimiento: Optional[str] = Form(None),
    dpi: Optional[str] = Form(None),
    telefono: Optional[str] = Form(None),
    tipo_sangre: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    service = AuthService(db)
    try:
        f_nac = date.fromisoformat(fecha_nacimiento) if fecha_nacimiento else None
        req = RegistroPacienteRequest(
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            password=password,
            fecha_nacimiento=f_nac,
            dpi=dpi,
            telefono=telefono,
            tipo_sangre=tipo_sangre
        )
        usuario = service.registrar_paciente(req)
        token = create_session_token(usuario.id)
        resp = RedirectResponse(url="/paciente/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        resp.set_cookie(
            key=settings.SESSION_COOKIE_NAME,
            value=token,
            httponly=True,
            max_age=86400,
            samesite="lax"
        )
        return resp
    except AppException as e:
        return templates.TemplateResponse(
            request=request,
            name="auth/registro.html",
            context={"error": e.message, "usuario_actual": None},
            status_code=400
        )


@router.post("/auth/web/logout")
def procesar_logout_web():
    resp = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    resp.delete_cookie(settings.SESSION_COOKIE_NAME)
    return resp

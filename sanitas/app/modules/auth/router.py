from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.core.security.session import create_session_token
from app.modules.auth.schemas import LoginRequest, RegistroPacienteRequest, AuthUserResponse
from app.modules.auth.service import AuthService
from app.modules.usuarios.models import Usuario
from app.core.dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=AuthUserResponse)
def login_api(
    data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    service = AuthService(db)
    usuario = service.autenticar(data)
    token = create_session_token(usuario.id)
    response.set_cookie(
        key=settings.SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        max_age=86400,
        samesite="lax"
    )
    return usuario


@router.post("/registro", response_model=AuthUserResponse, status_code=status.HTTP_201_CREATED)
def registro_paciente_api(
    data: RegistroPacienteRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    service = AuthService(db)
    usuario = service.registrar_paciente(data)
    token = create_session_token(usuario.id)
    response.set_cookie(
        key=settings.SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        max_age=86400,
        samesite="lax"
    )
    return usuario


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(settings.SESSION_COOKIE_NAME)
    return {"mensaje": "Sesión cerrada exitosamente"}


@router.get("/me", response_model=AuthUserResponse)
def obtener_perfil_actual(current_user: Usuario = Depends(get_current_user)):
    return current_user

from typing import Optional
from fastapi import Request, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.core.security.session import get_user_id_from_token
from app.core.exceptions import UnauthorizedError
from app.modules.usuarios.models import Usuario


def get_current_user_optional(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[Usuario]:
    """Obtiene el usuario en sesión actual si existe y está activo, o None."""
    token = request.cookies.get(settings.SESSION_COOKIE_NAME)
    if not token:
        # También admitir header si se usa API
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

    if not token:
        return None

    user_id = get_user_id_from_token(token)
    if not user_id:
        return None

    user = db.query(Usuario).filter(
        Usuario.id == user_id,
        Usuario.activo.is_(True)
    ).first()
    return user


def get_current_user(
    current_user: Optional[Usuario] = Depends(get_current_user_optional)
) -> Usuario:
    """Verifica que el usuario esté autenticado. Lanza UnauthorizedError si no."""
    if not current_user:
        raise UnauthorizedError("Debe iniciar sesión para acceder a este recurso.")
    return current_user

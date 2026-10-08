from typing import Optional
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from app.core.config import settings

_serializer = URLSafeTimedSerializer(settings.SECRET_KEY, salt="sanitas-session-salt")

# Sesión válida por 24 horas por defecto
SESSION_MAX_AGE_SECONDS = 86400


def create_session_token(user_id: int) -> str:
    """Genera un token de sesión firmado para el ID de usuario."""
    return _serializer.dumps({"user_id": user_id})


def get_user_id_from_token(token: str) -> Optional[int]:
    """Valida el token de sesión y extrae el ID de usuario."""
    if not token:
        return None
    try:
        data = _serializer.loads(token, max_age=SESSION_MAX_AGE_SECONDS)
        return data.get("user_id")
    except (BadSignature, SignatureExpired):
        return None

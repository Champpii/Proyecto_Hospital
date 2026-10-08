from typing import List, Callable
from fastapi import Depends
from app.core.dependencies.auth import get_current_user
from app.core.exceptions import ForbiddenError
from app.modules.usuarios.models import Usuario, RolUsuario


def require_roles(allowed_roles: List[str]) -> Callable[[Usuario], Usuario]:
    """Validador de dependencia de roles."""
    def role_checker(current_user: Usuario = Depends(get_current_user)) -> Usuario:
        if current_user.rol not in allowed_roles:
            raise ForbiddenError(
                f"No tiene permisos suficientes ({current_user.rol}) para esta acción."
            )
        return current_user
    return role_checker


# Shortcuts comunes
require_admin = require_roles([RolUsuario.ADMINISTRADOR.value])
require_medico_or_admin = require_roles([
    RolUsuario.MEDICO.value,
    RolUsuario.ADMINISTRADOR.value
])
require_paciente = require_roles([RolUsuario.PACIENTE.value])

from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.usuarios.models import Usuario, RolUsuario
from app.modules.usuarios.repository import UsuarioRepository
from app.modules.usuarios.schemas import UsuarioCreate, UsuarioUpdate, MedicoCreate
from app.core.security.password import hash_password
from app.core.exceptions import BusinessValidationError, NotFoundError


class UsuarioService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)

    def registrar_usuario(self, data: UsuarioCreate) -> Usuario:
        correo_limpio = data.correo.lower().strip()
        if self.repo.get_by_correo(correo_limpio):
            raise BusinessValidationError("El correo electrónico ya se encuentra registrado.")

        usuario = Usuario(
            nombre=data.nombre.strip(),
            apellido=data.apellido.strip(),
            correo=correo_limpio,
            password_hash=hash_password(data.password),
            rol=data.rol.value if isinstance(data.rol, RolUsuario) else data.rol,
            activo=True
        )
        return self.repo.create(usuario)

    def crear_medico(self, data: MedicoCreate) -> Usuario:
        create_dto = UsuarioCreate(
            nombre=data.nombre,
            apellido=data.apellido,
            correo=data.correo,
            password=data.password,
            rol=RolUsuario.MEDICO
        )
        return self.registrar_usuario(create_dto)

    def obtener_por_id(self, user_id: int) -> Usuario:
        usuario = self.repo.get_by_id(user_id)
        if not usuario:
            raise NotFoundError("Usuario no encontrado.")
        return usuario

    def listar_usuarios(self) -> List[Usuario]:
        return self.repo.get_all()

    def actualizar_usuario(self, user_id: int, data: UsuarioUpdate) -> Usuario:
        usuario = self.obtener_por_id(user_id)
        if data.nombre is not None:
            usuario.nombre = data.nombre.strip()
        if data.apellido is not None:
            usuario.apellido = data.apellido.strip()
        if data.correo is not None:
            correo_limpio = data.correo.lower().strip()
            existente = self.repo.get_by_correo(correo_limpio)
            if existente and existente.id != user_id:
                raise BusinessValidationError("El correo ya está en uso por otro usuario.")
            usuario.correo = correo_limpio
        if data.password:
            usuario.password_hash = hash_password(data.password)
        if data.activo is not None:
            usuario.activo = data.activo
        return self.repo.update(usuario)

    def cambiar_estado(self, user_id: int, activo: bool) -> Usuario:
        usuario = self.obtener_por_id(user_id)
        usuario.activo = activo
        return self.repo.update(usuario)

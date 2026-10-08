from sqlalchemy.orm import Session
from app.modules.auth.schemas import LoginRequest, RegistroPacienteRequest
from app.modules.usuarios.models import Usuario, RolUsuario
from app.modules.usuarios.repository import UsuarioRepository
from app.modules.pacientes.models import Paciente
from app.core.security.password import verify_password, hash_password
from app.core.exceptions import UnauthorizedError, BusinessValidationError


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UsuarioRepository(db)

    def autenticar(self, data: LoginRequest) -> Usuario:
        correo = data.correo.lower().strip()
        usuario = self.user_repo.get_by_correo(correo)
        if not usuario:
            raise UnauthorizedError("Credenciales inválidas.")

        if not usuario.activo:
            raise UnauthorizedError("Esta cuenta ha sido desactivada por la administración.")

        if not verify_password(data.password, usuario.password_hash):
            raise UnauthorizedError("Credenciales inválidas.")

        return usuario

    def registrar_paciente(self, data: RegistroPacienteRequest) -> Usuario:
        correo = data.correo.lower().strip()
        if self.user_repo.get_by_correo(correo):
            raise BusinessValidationError("El correo electrónico ya está registrado.")

        usuario = Usuario(
            nombre=data.nombre.strip(),
            apellido=data.apellido.strip(),
            correo=correo,
            password_hash=hash_password(data.password),
            rol=RolUsuario.PACIENTE.value,
            activo=True
        )
        self.db.add(usuario)
        self.db.flush()

        paciente = Paciente(
            usuario_id=usuario.id,
            fecha_nacimiento=data.fecha_nacimiento,
            dpi=data.dpi.strip() if data.dpi else None,
            telefono=data.telefono.strip() if data.telefono else None,
            tipo_sangre=data.tipo_sangre.strip().upper() if data.tipo_sangre else None
        )
        self.db.add(paciente)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

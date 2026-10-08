from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.pacientes.models import Paciente
from app.modules.pacientes.repository import PacienteRepository
from app.modules.pacientes.schemas import PacienteUpdate
from app.modules.usuarios.models import Usuario, RolUsuario
from app.core.exceptions import NotFoundError, ForbiddenError


class PacienteService:
    def __init__(self, db: Session):
        self.repo = PacienteRepository(db)

    def obtener_por_id(self, paciente_id: int) -> Paciente:
        paciente = self.repo.get_by_id(paciente_id)
        if not paciente:
            raise NotFoundError("Paciente no encontrado.")
        return paciente

    def obtener_por_usuario(self, usuario_id: int) -> Paciente:
        paciente = self.repo.get_by_usuario_id(usuario_id)
        if not paciente:
            raise NotFoundError("Perfil de paciente no encontrado.")
        return paciente

    def listar_o_buscar(self, query: Optional[str] = None) -> List[Paciente]:
        if query and query.strip():
            return self.repo.buscar(query)
        return self.repo.get_all()

    def actualizar_datos(
        self,
        paciente_id: int,
        data: PacienteUpdate,
        solicitante: Usuario
    ) -> Paciente:
        paciente = self.obtener_por_id(paciente_id)

        # Si el solicitante es paciente, solo puede editar sus propios datos
        if solicitante.rol == RolUsuario.PACIENTE.value and paciente.usuario_id != solicitante.id:
            raise ForbiddenError("No tiene permiso para modificar datos de otro paciente.")

        if data.telefono is not None:
            paciente.telefono = data.telefono.strip()
        if data.fecha_nacimiento is not None:
            paciente.fecha_nacimiento = data.fecha_nacimiento
        if data.tipo_sangre is not None:
            paciente.tipo_sangre = data.tipo_sangre.strip().upper()
        if data.dpi is not None:
            paciente.dpi = data.dpi.strip()

        # Actualizar datos del usuario asociado si vienen presentes
        if data.nombre is not None and data.nombre.strip():
            paciente.usuario.nombre = data.nombre.strip()
        if data.apellido is not None and data.apellido.strip():
            paciente.usuario.apellido = data.apellido.strip()

        return self.repo.update(paciente)

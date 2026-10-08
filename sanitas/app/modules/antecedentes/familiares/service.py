from typing import List
from sqlalchemy.orm import Session
from app.modules.antecedentes.familiares.models import AntecedenteFamiliar, EstadoEnfermedadFamiliar
from app.modules.antecedentes.familiares.repository import AntecedenteFamiliarRepository
from app.modules.antecedentes.familiares.schemas import AntecedenteFamiliarCreate, AntecedenteFamiliarUpdate
from app.modules.pacientes.repository import PacienteRepository
from app.modules.usuarios.models import Usuario, RolUsuario
from app.core.exceptions import NotFoundError, ForbiddenError


class AntecedenteFamiliarService:
    def __init__(self, db: Session):
        self.repo = AntecedenteFamiliarRepository(db)
        self.paciente_repo = PacienteRepository(db)

    def registrar(self, data: AntecedenteFamiliarCreate, solicitante: Usuario) -> AntecedenteFamiliar:
        if solicitante.rol not in [RolUsuario.MEDICO.value, RolUsuario.ADMINISTRADOR.value]:
            raise ForbiddenError("Solo los profesionales de la salud o administradores pueden registrar antecedentes.")

        paciente = self.paciente_repo.get_by_id(data.paciente_id)
        if not paciente:
            raise NotFoundError("El paciente especificado no existe.")

        item = AntecedenteFamiliar(
            paciente_id=data.paciente_id,
            registrado_por=solicitante.id,
            parentesco=data.parentesco.strip(),
            enfermedad=data.enfermedad.strip(),
            estado=data.estado.value if isinstance(data.estado, EstadoEnfermedadFamiliar) else data.estado,
            observaciones=data.observaciones.strip() if data.observaciones else None
        )
        return self.repo.create(item)

    def listar_por_paciente(self, paciente_id: int, solicitante: Usuario) -> List[AntecedenteFamiliar]:
        paciente = self.paciente_repo.get_by_id(paciente_id)
        if not paciente:
            raise NotFoundError("El paciente especificado no existe.")

        if (
            solicitante.rol == RolUsuario.PACIENTE.value
            and paciente.usuario_id != solicitante.id
        ):
            raise ForbiddenError("No tiene permiso para ver antecedentes de otro paciente.")

        return self.repo.get_by_paciente(paciente_id)

    def actualizar(
        self,
        ant_id: int,
        data: AntecedenteFamiliarUpdate,
        solicitante: Usuario
    ) -> AntecedenteFamiliar:
        if solicitante.rol not in [RolUsuario.MEDICO.value, RolUsuario.ADMINISTRADOR.value]:
            raise ForbiddenError("No tiene permisos para modificar antecedentes.")

        item = self.repo.get_by_id(ant_id)
        if not item:
            raise NotFoundError("Antecedente no encontrado.")

        if data.parentesco is not None:
            item.parentesco = data.parentesco.strip()
        if data.enfermedad is not None:
            item.enfermedad = data.enfermedad.strip()
        if data.estado is not None:
            item.estado = data.estado.value if isinstance(data.estado, EstadoEnfermedadFamiliar) else data.estado
        if data.observaciones is not None:
            item.observaciones = data.observaciones.strip()

        return self.repo.update(item)

    def eliminar(self, ant_id: int, solicitante: Usuario) -> None:
        if solicitante.rol not in [RolUsuario.MEDICO.value, RolUsuario.ADMINISTRADOR.value]:
            raise ForbiddenError("No tiene permisos para eliminar antecedentes.")

        item = self.repo.get_by_id(ant_id)
        if not item:
            raise NotFoundError("Antecedente no encontrado.")

        self.repo.delete(item)

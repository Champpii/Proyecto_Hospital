from typing import List
from sqlalchemy.orm import Session
from app.modules.antecedentes.personales.models import AntecedentePersonal, CategoriaPersonal
from app.modules.antecedentes.personales.repository import AntecedentePersonalRepository
from app.modules.antecedentes.personales.schemas import AntecedentePersonalCreate, AntecedentePersonalUpdate
from app.modules.pacientes.repository import PacienteRepository
from app.modules.usuarios.models import Usuario, RolUsuario
from app.core.exceptions import NotFoundError, ForbiddenError, BusinessValidationError


class AntecedentePersonalService:
    def __init__(self, db: Session):
        self.repo = AntecedentePersonalRepository(db)
        self.paciente_repo = PacienteRepository(db)

    def registrar(self, data: AntecedentePersonalCreate, solicitante: Usuario) -> AntecedentePersonal:
        if solicitante.rol not in [RolUsuario.MEDICO.value, RolUsuario.ADMINISTRADOR.value]:
            raise ForbiddenError("Solo los profesionales de la salud o administradores pueden registrar antecedentes.")

        paciente = self.paciente_repo.get_by_id(data.paciente_id)
        if not paciente:
            raise NotFoundError("El paciente especificado no existe.")

        item = AntecedentePersonal(
            paciente_id=data.paciente_id,
            registrado_por=solicitante.id,
            categoria=data.categoria.value if isinstance(data.categoria, CategoriaPersonal) else data.categoria,
            descripcion=data.descripcion.strip(),
            fecha=data.fecha,
            observaciones=data.observaciones.strip() if data.observaciones else None
        )
        return self.repo.create(item)

    def listar_por_paciente(self, paciente_id: int, solicitante: Usuario) -> List[AntecedentePersonal]:
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
        data: AntecedentePersonalUpdate,
        solicitante: Usuario
    ) -> AntecedentePersonal:
        if solicitante.rol not in [RolUsuario.MEDICO.value, RolUsuario.ADMINISTRADOR.value]:
            raise ForbiddenError("No tiene permisos para modificar antecedentes.")

        item = self.repo.get_by_id(ant_id)
        if not item:
            raise NotFoundError("Antecedente no encontrado.")

        if data.categoria is not None:
            item.categoria = data.categoria.value if isinstance(data.categoria, CategoriaPersonal) else data.categoria
        if data.descripcion is not None:
            item.descripcion = data.descripcion.strip()
        if data.fecha is not None:
            item.fecha = data.fecha
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

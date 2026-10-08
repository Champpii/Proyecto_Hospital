from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from app.modules.pacientes.models import Paciente
from app.modules.usuarios.models import Usuario


class PacienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, paciente_id: int) -> Optional[Paciente]:
        return (
            self.db.query(Paciente)
            .options(
                joinedload(Paciente.usuario),
                joinedload(Paciente.antecedentes_personales),
                joinedload(Paciente.antecedentes_familiares),
                joinedload(Paciente.archivos)
            )
            .filter(Paciente.id == paciente_id)
            .first()
        )

    def get_by_usuario_id(self, usuario_id: int) -> Optional[Paciente]:
        return (
            self.db.query(Paciente)
            .options(joinedload(Paciente.usuario))
            .filter(Paciente.usuario_id == usuario_id)
            .first()
        )

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Paciente]:
        return (
            self.db.query(Paciente)
            .join(Paciente.usuario)
            .options(joinedload(Paciente.usuario))
            .order_by(Usuario.apellido.asc(), Usuario.nombre.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def buscar(self, query: str) -> List[Paciente]:
        termino = f"%{query.strip().lower()}%"
        return (
            self.db.query(Paciente)
            .join(Paciente.usuario)
            .options(joinedload(Paciente.usuario))
            .filter(
                or_(
                    Usuario.nombre.ilike(termino),
                    Usuario.apellido.ilike(termino),
                    Usuario.correo.ilike(termino),
                    Paciente.dpi.ilike(termino),
                    Paciente.telefono.ilike(termino)
                )
            )
            .order_by(Usuario.apellido.asc())
            .all()
        )

    def update(self, paciente: Paciente) -> Paciente:
        self.db.commit()
        self.db.refresh(paciente)
        return paciente

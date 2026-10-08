from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.antecedentes.personales.models import AntecedentePersonal


class AntecedentePersonalRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, ant_id: int) -> Optional[AntecedentePersonal]:
        return self.db.query(AntecedentePersonal).filter(AntecedentePersonal.id == ant_id).first()

    def get_by_paciente(self, paciente_id: int) -> List[AntecedentePersonal]:
        return (
            self.db.query(AntecedentePersonal)
            .filter(AntecedentePersonal.paciente_id == paciente_id)
            .order_by(AntecedentePersonal.id.desc())
            .all()
        )

    def create(self, item: AntecedentePersonal) -> AntecedentePersonal:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item: AntecedentePersonal) -> AntecedentePersonal:
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: AntecedentePersonal) -> None:
        self.db.delete(item)
        self.db.commit()

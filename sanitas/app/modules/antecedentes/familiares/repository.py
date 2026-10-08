from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.antecedentes.familiares.models import AntecedenteFamiliar


class AntecedenteFamiliarRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, ant_id: int) -> Optional[AntecedenteFamiliar]:
        return self.db.query(AntecedenteFamiliar).filter(AntecedenteFamiliar.id == ant_id).first()

    def get_by_paciente(self, paciente_id: int) -> List[AntecedenteFamiliar]:
        return (
            self.db.query(AntecedenteFamiliar)
            .filter(AntecedenteFamiliar.paciente_id == paciente_id)
            .order_by(AntecedenteFamiliar.id.desc())
            .all()
        )

    def create(self, item: AntecedenteFamiliar) -> AntecedenteFamiliar:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item: AntecedenteFamiliar) -> AntecedenteFamiliar:
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: AntecedenteFamiliar) -> None:
        self.db.delete(item)
        self.db.commit()

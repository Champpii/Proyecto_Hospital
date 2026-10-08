from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.archivos.models import Archivo


class ArchivoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, archivo_id: int) -> Optional[Archivo]:
        return self.db.query(Archivo).filter(Archivo.id == archivo_id).first()

    def get_by_paciente(self, paciente_id: int) -> List[Archivo]:
        return (
            self.db.query(Archivo)
            .filter(Archivo.paciente_id == paciente_id)
            .order_by(Archivo.id.desc())
            .all()
        )

    def create(self, archivo: Archivo) -> Archivo:
        self.db.add(archivo)
        self.db.commit()
        self.db.refresh(archivo)
        return archivo

    def delete(self, archivo: Archivo) -> None:
        self.db.delete(archivo)
        self.db.commit()

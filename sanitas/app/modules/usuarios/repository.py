from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.usuarios.models import Usuario


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.id == user_id).first()

    def get_by_correo(self, correo: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.correo == correo.lower().strip()).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        return self.db.query(Usuario).offset(skip).limit(limit).all()

    def get_by_rol(self, rol: str) -> List[Usuario]:
        return self.db.query(Usuario).filter(Usuario.rol == rol).all()

    def create(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def update(self, usuario: Usuario) -> Usuario:
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def delete(self, usuario: Usuario) -> None:
        self.db.delete(usuario)
        self.db.commit()

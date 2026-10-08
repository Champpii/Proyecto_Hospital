from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base


class RolUsuario(str, Enum):
    PACIENTE = "paciente"
    MEDICO = "medico"
    ADMINISTRADOR = "administrador"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    correo = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(20), nullable=False, default=RolUsuario.PACIENTE.value)
    activo = Column(Boolean, default=True, nullable=False)
    creado_en = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relación uno a uno con Paciente (si rol es paciente)
    paciente = relationship(
        "Paciente",
        back_populates="usuario",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Usuario {self.correo} ({self.rol})>"

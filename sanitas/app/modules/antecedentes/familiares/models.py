from enum import Enum
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class EstadoEnfermedadFamiliar(str, Enum):
    PASADA = "pasada"
    ACTUAL = "actual"


class AntecedenteFamiliar(Base):
    __tablename__ = "antecedentes_familiares"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(
        Integer,
        ForeignKey("pacientes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    registrado_por = Column(
        Integer,
        ForeignKey("usuarios.id", ondelete="SET NULL"),
        nullable=True
    )
    parentesco = Column(String(50), nullable=False)
    enfermedad = Column(String(255), nullable=False)
    estado = Column(
        String(20),
        nullable=False,
        default=EstadoEnfermedadFamiliar.ACTUAL.value
    )
    observaciones = Column(Text, nullable=True)

    # Relaciones
    paciente = relationship("Paciente", back_populates="antecedentes_familiares")
    registrador = relationship("Usuario", foreign_keys=[registrado_por])

    def __repr__(self):
        return f"<AntecedenteFamiliar id={self.id} parentesco={self.parentesco}>"

from enum import Enum
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class CategoriaPersonal(str, Enum):
    ALERGIA = "alergia"
    ENFERMEDAD = "enfermedad"
    CIRUGIA = "cirugia"
    VACUNA = "vacuna"
    MEDICAMENTO = "medicamento"
    HABITO = "habito"


class AntecedentePersonal(Base):
    __tablename__ = "antecedentes_personales"

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
    categoria = Column(String(50), nullable=False)
    descripcion = Column(String(255), nullable=False)
    fecha = Column(Date, nullable=True)
    observaciones = Column(Text, nullable=True)

    # Relaciones
    paciente = relationship("Paciente", back_populates="antecedentes_personales")
    registrador = relationship("Usuario", foreign_keys=[registrado_por])

    def __repr__(self):
        return f"<AntecedentePersonal id={self.id} cat={self.categoria}>"

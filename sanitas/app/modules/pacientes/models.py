from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
    fecha_nacimiento = Column(Date, nullable=True)
    dpi = Column(String(30), nullable=True, index=True)
    telefono = Column(String(30), nullable=True)
    tipo_sangre = Column(String(10), nullable=True)

    # Relaciones
    usuario = relationship("Usuario", back_populates="paciente")
    antecedentes_personales = relationship(
        "AntecedentePersonal",
        back_populates="paciente",
        cascade="all, delete-orphan",
        order_by="AntecedentePersonal.id.desc()"
    )
    antecedentes_familiares = relationship(
        "AntecedenteFamiliar",
        back_populates="paciente",
        cascade="all, delete-orphan",
        order_by="AntecedenteFamiliar.id.desc()"
    )
    archivos = relationship(
        "Archivo",
        back_populates="paciente",
        cascade="all, delete-orphan",
        order_by="Archivo.id.desc()"
    )

    def __repr__(self):
        return f"<Paciente id={self.id} usuario_id={self.usuario_id}>"

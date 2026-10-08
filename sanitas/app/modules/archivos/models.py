from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, LargeBinary, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Archivo(Base):
    __tablename__ = "archivos"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(
        Integer,
        ForeignKey("pacientes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    subido_por = Column(
        Integer,
        ForeignKey("usuarios.id", ondelete="SET NULL"),
        nullable=True
    )
    nombre_archivo = Column(String(255), nullable=False)
    tipo_mime = Column(String(100), nullable=False)
    tamano = Column(Integer, nullable=False)  # En bytes
    contenido = Column(LargeBinary, nullable=False)  # bytea en PostgreSQL
    descripcion = Column(Text, nullable=True)
    creado_en = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    paciente = relationship("Paciente", back_populates="archivos")
    autor = relationship("Usuario", foreign_keys=[subido_por])

    def __repr__(self):
        return f"<Archivo id={self.id} nombre={self.nombre_archivo}>"

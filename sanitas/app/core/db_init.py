from app.core.database import Base, engine
# Importar todos los modelos para registrarlos en los metadatos de SQLAlchemy
from app.modules.usuarios.models import Usuario  # noqa: F401
from app.modules.pacientes.models import Paciente  # noqa: F401
from app.modules.antecedentes.personales.models import AntecedentePersonal  # noqa: F401
from app.modules.antecedentes.familiares.models import AntecedenteFamiliar  # noqa: F401
from app.modules.archivos.models import Archivo  # noqa: F401


def init_db():
    """Crea todas las tablas de la base de datos si no existen."""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Tablas inicializadas correctamente.")

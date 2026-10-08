import sys
import os

# Asegurar que el directorio raíz de la app esté en sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import SessionLocal
from app.core.db_init import init_db
from app.modules.usuarios.models import Usuario, RolUsuario
from app.core.security.password import hash_password


def crear_primer_admin(nombre="Admin", apellido="Sanitas", correo="admin@sanitas.com", password="admin12345"):
    print("Inicializando base de datos si no existe...")
    init_db()

    db = SessionLocal()
    try:
        existente = db.query(Usuario).filter(Usuario.correo == correo.lower().strip()).first()
        if existente:
            print(f"El usuario con correo {correo} ya existe (Rol: {existente.rol}).")
            return existente

        admin = Usuario(
            nombre=nombre,
            apellido=apellido,
            correo=correo.lower().strip(),
            password_hash=hash_password(password),
            rol=RolUsuario.ADMINISTRADOR.value,
            activo=True
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print("==========================================")
        print(" Administrador creado exitosamente:")
        print(f" Correo: {admin.correo}")
        print(f" Contraseña: {password}")
        print(f" Rol: {admin.rol}")
        print("==========================================")
        return admin
    finally:
        db.close()


if __name__ == "__main__":
    nombre = input("Nombre [Admin]: ").strip() or "Admin"
    apellido = input("Apellido [Sanitas]: ").strip() or "Sanitas"
    correo = input("Correo [admin@sanitas.com]: ").strip() or "admin@sanitas.com"
    password = input("Contraseña [admin12345]: ").strip() or "admin12345"

    crear_primer_admin(nombre, apellido, correo, password)

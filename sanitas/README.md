# Hospital Sanitas - Sistema de Historial Médico (Prototipo)

Prototipo funcional del sistema de historial médico desarrollado con **FastAPI**, **SQLAlchemy**, **PostgreSQL / SQLite**, **HTML5/Jinja2** y **CSS puro**.

---

## 1. Características Implementadas

- **Autenticación y Seguridad**:
  - Hash de contraseñas con `bcrypt`.
  - Sesiones firmadas con cookies seguras (`itsdangerous`).
  - Control de acceso basado en roles: `paciente`, `medico` y `administrador`.

- **Módulos Clínicos y de Usuarios**:
  - **Auto-registro de Pacientes**: Creación de usuario y perfil de paciente asociado.
  - **Gestión Médica**: Búsqueda en tiempo real por nombre, apellido, correo o DPI.
  - **Antecedentes Personales**: Registro de alergias, cirugías, enfermedades, vacunas, medicamentos y hábitos.
  - **Antecedentes Familiares**: Parentesco, patología, estado (actual o pasada) y observaciones.
  - **Adjuntos Médicos**: Almacenamiento directo en base de datos (`bytea` / `LargeBinary`), con soporte para PDF, PNG y JPG hasta 5 MB.
  - **Panel de Administración**: Métricas globales, creación de cuentas de médicos y activación/desactivación de usuarios.

- **Diseño Limpio**:
  - CSS modular sin frameworks pesados, dividido en `base`, `components` y `pages`.
  - Componentes reutilizables con plantillas Jinja2.
  - Ningún archivo supera las 250 líneas de código.

---

## 2. Estructura del Proyecto

```
sanitas/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── db_init.py
│   │   ├── exceptions.py
│   │   ├── security/
│   │   └── dependencies/
│   ├── modules/
│   │   ├── auth/
│   │   ├── usuarios/
│   │   ├── pacientes/
│   │   ├── antecedentes/
│   │   │   ├── personales/
│   │   │   └── familiares/
│   │   └── archivos/
│   └── web/
│       ├── templates/
│       │   ├── base/
│       │   ├── components/
│       │   ├── auth/
│       │   ├── paciente/
│       │   ├── medico/
│       │   └── admin/
│       └── static/
│           └── css/
├── scripts/
│   └── crear_admin.py
├── tests/
│   ├── conftest.py
│   └── test_sanitas.py
├── requirements.txt
└── .env.example
```

---

## 3. Puesta en Marcha

### 3.1. Requisitos e Instalación
```bash
pip install -r requirements.txt
```

### 3.2. Configuración de Base de Datos
Copiar `.env.example` a `.env`:
```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/sanitas_db
MAX_FILE_SIZE_MB=5
ALLOWED_MIME_TYPES=application/pdf,image/png,image/jpeg
```
*(Si no se define o no hay PostgreSQL corriendo, se utiliza automáticamente `sqlite:///./sanitas_dev.db` para pruebas locales inmediatas).*

### 3.3. Crear el Administrador Inicial
```bash
python scripts/crear_admin.py
```
Credenciales por defecto:
- **Correo**: `admin@sanitas.com`
- **Contraseña**: `admin12345`

### 3.4. Ejecutar el Servidor
Desde la carpeta `sanitas/`:
```bash
uvicorn app.main:app --reload --port 8000
```
Abrir en el navegador: [http://localhost:8000](http://localhost:8000)

---

## 4. Pruebas Automatizadas
Ejecutar la suite de pruebas unitarias y de integración:
```bash
pytest
```
Todas las pruebas de roles, permisos, historial médico y subida/descarga de adjuntos se ejecutan en entorno aislado.

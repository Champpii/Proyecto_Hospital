import io
from app.modules.usuarios.models import Usuario, RolUsuario
from app.core.security.password import hash_password, verify_password
from app.core.security.session import create_session_token
from app.core.config import settings


def test_password_hash():
    pwd = "SecretPassword123"
    hashed = hash_password(pwd)
    assert verify_password(pwd, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_registro_y_login_paciente(client):
    # Registro de paciente
    payload = {
        "nombre": "Juan",
        "apellido": "Perez",
        "correo": "juan.perez@sanitas.com",
        "password": "password123",
        "fecha_nacimiento": "1990-05-15",
        "dpi": "1234567890101",
        "telefono": "5551234",
        "tipo_sangre": "O+"
    }
    res_reg = client.post("/api/auth/registro", json=payload)
    assert res_reg.status_code == 201
    data = res_reg.json()
    assert data["correo"] == "juan.perez@sanitas.com"
    assert data["rol"] == "paciente"

    # Login exitoso
    res_log = client.post("/api/auth/login", json={
        "correo": "juan.perez@sanitas.com",
        "password": "password123"
    })
    assert res_log.status_code == 200
    assert settings.SESSION_COOKIE_NAME in res_log.cookies


def test_creacion_medico_por_admin(client, db_session):
    # Crear admin en BD
    admin = Usuario(
        nombre="Admin",
        apellido="Sanitas",
        correo="admin.test@sanitas.com",
        password_hash=hash_password("adminpass"),
        rol=RolUsuario.ADMINISTRADOR.value,
        activo=True
    )
    db_session.add(admin)
    db_session.commit()

    admin_token = create_session_token(admin.id)
    client.cookies.set(settings.SESSION_COOKIE_NAME, admin_token)

    # Admin crea médico
    medico_data = {
        "nombre": "Carlos",
        "apellido": "Gomez",
        "correo": "dr.gomez@sanitas.com",
        "password": "medicopassword"
    }
    res = client.post("/api/usuarios/medicos", json=medico_data)
    assert res.status_code == 201
    assert res.json()["rol"] == "medico"


def test_antecedentes_y_adjuntos(client, db_session):
    # Crear médico y paciente
    medico = Usuario(
        nombre="Dra. Maria",
        apellido="Lopez",
        correo="dra.lopez@sanitas.com",
        password_hash=hash_password("medpass"),
        rol=RolUsuario.MEDICO.value,
        activo=True
    )
    db_session.add(medico)
    db_session.commit()

    # Registrar paciente
    paciente_res = client.post("/api/auth/registro", json={
        "nombre": "Ana",
        "apellido": "Morales",
        "correo": "ana.morales@sanitas.com",
        "password": "anapassword",
        "tipo_sangre": "A+"
    })
    ana_user_id = paciente_res.json()["id"]

    # Autenticar como médico
    medico_token = create_session_token(medico.id)
    client.cookies.set(settings.SESSION_COOKIE_NAME, medico_token)

    # Obtener paciente ID
    res_list = client.get("/api/pacientes/?q=Ana")
    assert res_list.status_code == 200
    pacientes = res_list.json()
    assert len(pacientes) > 0
    paciente_id = pacientes[0]["id"]

    # Médico registra antecedente personal
    ant_personal = {
        "paciente_id": paciente_id,
        "categoria": "alergia",
        "descripcion": "Alergia severa a penicilina",
        "fecha": "2020-01-10",
        "observaciones": "Produce urticaria"
    }
    res_ant_p = client.post("/api/antecedentes/personales/", json=ant_personal)
    assert res_ant_p.status_code == 201
    ant_p_id = res_ant_p.json()["id"]

    # Médico registra antecedente familiar
    ant_familiar = {
        "paciente_id": paciente_id,
        "parentesco": "Madre",
        "enfermedad": "Diabetes Mellitus Tipo 2",
        "estado": "actual",
        "observaciones": "Controlada con metformina"
    }
    res_ant_f = client.post("/api/antecedentes/familiares/", json=ant_familiar)
    assert res_ant_f.status_code == 201

    # Subir adjunto PDF
    fake_pdf = io.BytesIO(b"%PDF-1.4 Fake PDF Content")
    files = {"archivo": ("laboratorio.pdf", fake_pdf, "application/pdf")}
    data = {"paciente_id": paciente_id, "descripcion": "Examen de sangre"}
    res_file = client.post("/api/archivos/subir", data=data, files=files)
    assert res_file.status_code == 201
    archivo_id = res_file.json()["id"]

    # Descargar adjunto
    res_dl = client.get(f"/api/archivos/{archivo_id}/descargar")
    assert res_dl.status_code == 200
    assert res_dl.content == b"%PDF-1.4 Fake PDF Content"

    # Paciente consulta sus antecedentes y archivo
    paciente_token = create_session_token(ana_user_id)
    client.cookies.set(settings.SESSION_COOKIE_NAME, paciente_token)

    res_my_ant = client.get(f"/api/antecedentes/personales/paciente/{paciente_id}")
    assert res_my_ant.status_code == 200
    assert len(res_my_ant.json()) >= 1

    # Paciente NO tiene permiso para crear antecedentes
    res_forbidden = client.post("/api/antecedentes/personales/", json=ant_personal)
    assert res_forbidden.status_code == 403

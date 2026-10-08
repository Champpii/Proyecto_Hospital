from datetime import date
from typing import Optional
from fastapi import APIRouter, Request, Depends, Form, UploadFile, File, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies.roles import require_medico_or_admin
from app.modules.pacientes.service import PacienteService
from app.modules.antecedentes.personales.service import AntecedentePersonalService
from app.modules.antecedentes.personales.schemas import AntecedentePersonalCreate
from app.modules.antecedentes.familiares.service import AntecedenteFamiliarService
from app.modules.antecedentes.familiares.schemas import AntecedenteFamiliarCreate
from pathlib import Path
from app.modules.archivos.service import ArchivoService
from app.modules.usuarios.models import Usuario

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
router = APIRouter(prefix="/medico", tags=["Web Médico"])


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_medico(
    request: Request,
    q: Optional[str] = None,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_medico_or_admin)
):
    paciente_service = PacienteService(db)
    pacientes = paciente_service.listar_o_buscar(q)
    return templates.TemplateResponse(
        request=request,
        name="medico/dashboard.html",
        context={"usuario_actual": usuario, "pacientes": pacientes, "q": q}
    )


@router.get("/pacientes/{paciente_id}", response_class=HTMLResponse)
def ver_historial(
    paciente_id: int,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_medico_or_admin)
):
    paciente_service = PacienteService(db)
    paciente = paciente_service.obtener_por_id(paciente_id)
    return templates.TemplateResponse(
        request=request,
        name="medico/historial_paciente.html",
        context={"usuario_actual": usuario, "paciente": paciente}
    )


@router.post("/pacientes/{paciente_id}/antecedentes-personales")
def agregar_antecedente_personal(
    paciente_id: int,
    categoria: str = Form(...),
    descripcion: str = Form(...),
    fecha: Optional[str] = Form(None),
    observaciones: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_medico_or_admin)
):
    service = AntecedentePersonalService(db)
    f_ant = date.fromisoformat(fecha) if fecha else None
    dto = AntecedentePersonalCreate(
        paciente_id=paciente_id,
        categoria=categoria,
        descripcion=descripcion,
        fecha=f_ant,
        observaciones=observaciones
    )
    service.registrar(dto, usuario)
    return RedirectResponse(
        url=f"/medico/pacientes/{paciente_id}",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/pacientes/{paciente_id}/antecedentes-personales/{ant_id}/eliminar")
def eliminar_antecedente_personal(
    paciente_id: int,
    ant_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_medico_or_admin)
):
    service = AntecedentePersonalService(db)
    service.eliminar(ant_id, usuario)
    return RedirectResponse(
        url=f"/medico/pacientes/{paciente_id}",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/pacientes/{paciente_id}/antecedentes-familiares")
def agregar_antecedente_familiar(
    paciente_id: int,
    parentesco: str = Form(...),
    enfermedad: str = Form(...),
    estado: str = Form("actual"),
    observaciones: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_medico_or_admin)
):
    service = AntecedenteFamiliarService(db)
    dto = AntecedenteFamiliarCreate(
        paciente_id=paciente_id,
        parentesco=parentesco,
        enfermedad=enfermedad,
        estado=estado,
        observaciones=observaciones
    )
    service.registrar(dto, usuario)
    return RedirectResponse(
        url=f"/medico/pacientes/{paciente_id}",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/pacientes/{paciente_id}/antecedentes-familiares/{ant_id}/eliminar")
def eliminar_antecedente_familiar(
    paciente_id: int,
    ant_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_medico_or_admin)
):
    service = AntecedenteFamiliarService(db)
    service.eliminar(ant_id, usuario)
    return RedirectResponse(
        url=f"/medico/pacientes/{paciente_id}",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/pacientes/{paciente_id}/archivos")
async def subir_archivo_medico(
    paciente_id: int,
    archivo: UploadFile = File(...),
    descripcion: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_medico_or_admin)
):
    service = ArchivoService(db)
    await service.guardar_archivo(
        paciente_id=paciente_id,
        upload_file=archivo,
        descripcion=descripcion,
        solicitante=usuario
    )
    return RedirectResponse(
        url=f"/medico/pacientes/{paciente_id}",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.post("/pacientes/{paciente_id}/archivos/{archivo_id}/eliminar")
def eliminar_archivo_medico(
    paciente_id: int,
    archivo_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_medico_or_admin)
):
    service = ArchivoService(db)
    service.eliminar_archivo(archivo_id, usuario)
    return RedirectResponse(
        url=f"/medico/pacientes/{paciente_id}",
        status_code=status.HTTP_303_SEE_OTHER
    )

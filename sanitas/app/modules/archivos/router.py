import urllib.parse
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, Response, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies.auth import get_current_user
from app.modules.archivos.schemas import ArchivoResponse
from app.modules.archivos.service import ArchivoService
from app.modules.usuarios.models import Usuario

router = APIRouter(prefix="/archivos", tags=["Archivos"])


@router.post("/subir", response_model=ArchivoResponse, status_code=status.HTTP_201_CREATED)
async def subir_archivo(
    paciente_id: int = Form(...),
    descripcion: Optional[str] = Form(None),
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    service = ArchivoService(db)
    return await service.guardar_archivo(
        paciente_id=paciente_id,
        upload_file=archivo,
        descripcion=descripcion,
        solicitante=current_user
    )


@router.get("/paciente/{paciente_id}", response_model=List[ArchivoResponse])
def listar_archivos_paciente(
    paciente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    service = ArchivoService(db)
    return service.listar_por_paciente(paciente_id, current_user)


@router.get("/{archivo_id}/descargar")
def descargar_archivo(
    archivo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    service = ArchivoService(db)
    archivo = service.obtener_archivo(archivo_id, current_user)
    # Codificar nombre de archivo para evitar problemas con acentos o espacios
    encoded_filename = urllib.parse.quote(archivo.nombre_archivo)
    headers = {
        "Content-Disposition": f"inline; filename*=UTF-8''{encoded_filename}"
    }
    return Response(
        content=archivo.contenido,
        media_type=archivo.tipo_mime,
        headers=headers
    )


@router.delete("/{archivo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_archivo(
    archivo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    service = ArchivoService(db)
    service.eliminar_archivo(archivo_id, current_user)
    return None

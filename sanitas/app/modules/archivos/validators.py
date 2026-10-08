import os
from fastapi import UploadFile
from app.core.config import settings
from app.core.exceptions import BusinessValidationError

EXTENSIONES_PERMITIDAS = {".pdf", ".png", ".jpg", ".jpeg"}
MIME_PERMITIDOS = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/pjpeg"
}


def validar_archivo_subida(archivo: UploadFile, contenido_bytes: bytes) -> None:
    """Valida la extensión, tipo MIME y tamaño del archivo adjunto."""
    if not archivo.filename:
        raise BusinessValidationError("El archivo no tiene un nombre válido.")

    ext = os.path.splitext(archivo.filename)[1].lower()
    if ext not in EXTENSIONES_PERMITIDAS:
        raise BusinessValidationError(
            f"Formato no permitido ({ext}). Solo se admiten archivos PDF, PNG y JPG."
        )

    if archivo.content_type and archivo.content_type.lower() not in MIME_PERMITIDOS:
        raise BusinessValidationError(
            f"Tipo MIME no admitido: {archivo.content_type}. Solo PDF, PNG y JPG."
        )

    tamano = len(contenido_bytes)
    if tamano == 0:
        raise BusinessValidationError("El archivo seleccionado está vacío.")

    if tamano > settings.MAX_FILE_SIZE_BYTES:
        raise BusinessValidationError(
            f"El archivo excede el tamaño máximo permitido de {settings.MAX_FILE_SIZE_MB} MB."
        )

from typing import List, Optional
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.modules.archivos.models import Archivo
from app.modules.archivos.repository import ArchivoRepository
from app.modules.archivos.validators import validar_archivo_subida
from app.modules.pacientes.repository import PacienteRepository
from app.modules.usuarios.models import Usuario, RolUsuario
from app.core.exceptions import NotFoundError, ForbiddenError


class ArchivoService:
    def __init__(self, db: Session):
        self.repo = ArchivoRepository(db)
        self.paciente_repo = PacienteRepository(db)

    async def guardar_archivo(
        self,
        paciente_id: int,
        upload_file: UploadFile,
        descripcion: Optional[str],
        solicitante: Usuario
    ) -> Archivo:
        if solicitante.rol not in [RolUsuario.MEDICO.value, RolUsuario.ADMINISTRADOR.value]:
            raise ForbiddenError("Solo el personal médico o administradores pueden subir adjuntos.")

        paciente = self.paciente_repo.get_by_id(paciente_id)
        if not paciente:
            raise NotFoundError("El paciente especificado no existe.")

        contenido = await upload_file.read()
        validar_archivo_subida(upload_file, contenido)

        archivo = Archivo(
            paciente_id=paciente_id,
            subido_por=solicitante.id,
            nombre_archivo=upload_file.filename,
            tipo_mime=upload_file.content_type or "application/octet-stream",
            tamano=len(contenido),
            contenido=contenido,
            descripcion=descripcion.strip() if descripcion else None
        )
        return self.repo.create(archivo)

    def obtener_archivo(self, archivo_id: int, solicitante: Usuario) -> Archivo:
        archivo = self.repo.get_by_id(archivo_id)
        if not archivo:
            raise NotFoundError("Archivo no encontrado.")

        # Verificar permisos
        if solicitante.rol == RolUsuario.PACIENTE.value:
            paciente = self.paciente_repo.get_by_id(archivo.paciente_id)
            if not paciente or paciente.usuario_id != solicitante.id:
                raise ForbiddenError("No tiene permiso para acceder a este archivo.")

        return archivo

    def listar_por_paciente(self, paciente_id: int, solicitante: Usuario) -> List[Archivo]:
        paciente = self.paciente_repo.get_by_id(paciente_id)
        if not paciente:
            raise NotFoundError("El paciente no existe.")

        if (
            solicitante.rol == RolUsuario.PACIENTE.value
            and paciente.usuario_id != solicitante.id
        ):
            raise ForbiddenError("No tiene permiso para consultar archivos de otro paciente.")

        return self.repo.get_by_paciente(paciente_id)

    def eliminar_archivo(self, archivo_id: int, solicitante: Usuario) -> None:
        if solicitante.rol not in [RolUsuario.MEDICO.value, RolUsuario.ADMINISTRADOR.value]:
            raise ForbiddenError("No tiene permiso para eliminar archivos.")

        archivo = self.repo.get_by_id(archivo_id)
        if not archivo:
            raise NotFoundError("Archivo no encontrado.")

        self.repo.delete(archivo)

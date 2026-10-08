from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse
from app.core.config import settings
from app.core.db_init import init_db
from app.core.exceptions import AppException, UnauthorizedError, ForbiddenError

# Routers de la API
from app.modules.auth.router import router as api_auth_router
from app.modules.usuarios.router import router as api_usuarios_router
from app.modules.pacientes.router import router as api_pacientes_router
from app.modules.antecedentes.router import router as api_antecedentes_router
from app.modules.archivos.router import router as api_archivos_router

# Router de la Interfaz Web Jinja2
from app.web.router import router as web_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Sistema de Historial Médico - Hospital Sanitas",
    version="1.0.0",
    lifespan=lifespan
)

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "web" / "static"

# Montar archivos estáticos CSS
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# Manejador de excepciones
@app.exception_handler(UnauthorizedError)
async def unauthorized_handler(request: Request, exc: UnauthorizedError):
    if request.url.path.startswith("/api/"):
        return JSONResponse(status_code=401, content={"detail": exc.message})
    # Para vistas web, redirigir a login
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


@app.exception_handler(ForbiddenError)
async def forbidden_handler(request: Request, exc: ForbiddenError):
    if request.url.path.startswith("/api/"):
        return JSONResponse(status_code=403, content={"detail": exc.message})
    return JSONResponse(status_code=403, content={"detail": exc.message})


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


# Registrar routers de la API REST
app.include_router(api_auth_router, prefix="/api")
app.include_router(api_usuarios_router, prefix="/api")
app.include_router(api_pacientes_router, prefix="/api")
app.include_router(api_antecedentes_router, prefix="/api")
app.include_router(api_archivos_router, prefix="/api")

# Registrar vistas web Jinja2
app.include_router(web_router)

from fastapi import APIRouter
from app.web.views_auth import router as auth_web_router
from app.web.views_paciente import router as paciente_web_router
from app.web.views_medico import router as medico_web_router
from app.web.views_admin import router as admin_web_router

router = APIRouter()
router.include_router(auth_web_router)
router.include_router(paciente_web_router)
router.include_router(medico_web_router)
router.include_router(admin_web_router)

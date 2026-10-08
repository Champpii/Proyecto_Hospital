from fastapi import APIRouter
from app.modules.antecedentes.personales.router import router as personales_router
from app.modules.antecedentes.familiares.router import router as familiares_router

router = APIRouter(prefix="/antecedentes", tags=["Antecedentes"])
router.include_router(personales_router)
router.include_router(familiares_router)

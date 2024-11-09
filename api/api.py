from api.auth import get_api_key
from fastapi import (APIRouter,
                     Depends,
                     Request)
from .limiter import limiter

from .routes.consulta_invitados import router as consulta_invitados_router
from .routes.consulta_premios import router as consulta_premios_router
from .routes.invitados import router as invitados_router
from .routes.premios import router as premios_router
from .routes.carga_masiva import router as carga_masiva_router
from .routes.reset_db import router as reset_db_router


api_router = APIRouter()


api_router.include_router(consulta_invitados_router,
                          prefix="/consulta_invitados",
                          dependencies=[Depends(get_api_key)])

api_router.include_router(consulta_premios_router,
                          prefix="/consulta_premios",
                          dependencies=[Depends(get_api_key)])

api_router.include_router(invitados_router,
                          prefix="/invitados",
                          dependencies=[Depends(get_api_key)])

api_router.include_router(premios_router,
                          prefix="/premios",
                          dependencies=[Depends(get_api_key)])

api_router.include_router(carga_masiva_router,
                          prefix="/carga_masiva",
                          dependencies=[Depends(get_api_key)])

api_router.include_router(reset_db_router,
                          prefix="/reset_db",
                          dependencies=[Depends(get_api_key)])


@api_router.get("/",
                summary="API Overview",
                dependencies=[Depends(get_api_key)])
@limiter.limit("2/minute")
async def api_overview(request: Request):
    return {
        "name": "VITA Fiesta",
        "version": "1.3.1",
        "Swagger documentation": "Visitar /docs",
        "endpoints": {
            "/consulta_invitados": "GET invitados",
            "/consulta_premios": "GET premios",
            "/consulta_invitados/{telefono}": "GET invitado",  # En-fiesta
            "/consulta_premios/{telefono}": "GET premio",  # En-fiesta
            "/invitados": "PUT invitados",  # Pre-fiesta
            "/premios": "PUT premios",  # Post-fiesta
            "/carga_masiva": "POST invitados y premios",
            "/reset_db": "POST resetear base de datos"
        },
        "rate_limits": "5 requests por minuto"
    }

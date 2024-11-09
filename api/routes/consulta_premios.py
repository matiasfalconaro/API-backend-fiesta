from database.crud import (get_db,
                           get_premio,
                           get_all_premios)
from database.models import Invitados
from fastapi import (APIRouter,
                     Depends,
                     HTTPException,
                     Request)
from ..limiter import limiter                     
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/")
@limiter.limit("25/minute")
async def obtener_todos_premios(request: Request,
                                db: Session = Depends(get_db),):
    """
    Endpoint para obtener todos los invitados de la base de datos.
    """
    premios = get_all_premios(db)
    return {"premios": premios}


@router.get("/{telefono_invitado}")
@limiter.limit("5/minute")
async def obtener_premio_por_telefono(request: Request,
                                      telefono_invitado: int,
                                      db: Session = Depends(get_db)):
    """
    Endpoint para obtener un premio por el número de teléfono del invitado.
    """
    premio = get_premio(db, telefono_invitado)
    
    if not premio:
        raise HTTPException(status_code=404, detail="Premio no encontrado")
    
    return {"premio": premio}

from database.crud import (get_db,
                           get_all_invitados,
                           get_invitado)
from fastapi import (APIRouter,
                     Depends,
                     HTTPException,
                     Request)
from ..limiter import limiter
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/")
@limiter.limit("5/minute")
async def obtener_todos_invitados(request: Request,
                                  db: Session = Depends(get_db)):
    """
    Endpoint para obtener todos los invitados de la base de datos.
    """
    invitados = get_all_invitados(db)
    return {"invitados": invitados}


@router.get("/{telefono}")
@limiter.limit("25/minute")
async def obtener_invitado_por_telefono(request: Request,
                                        telefono: int,
                                        db: Session = Depends(get_db)):
    """
    Endpoint para obtener un invitado por su número de teléfono.
    """
    invitado = get_invitado(db, telefono)
    
    if not invitado:
        raise HTTPException(status_code=404, detail="Invitado no encontrado")
    
    return {"invitado": invitado}

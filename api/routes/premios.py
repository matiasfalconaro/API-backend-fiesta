from database.crud import (get_db,
                           get_invitado,
                           update_premio)
from fastapi import (APIRouter,
                     Depends,
                     HTTPException,
                     Request)
from ..limiter import limiter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
from database.models import Premios


router = APIRouter()


class PremioAsignacionData(BaseModel):
    """
    Modelo Pydantic (campos opcionales)
    """
    codigo_premio: str
    premio: Optional[str] = None
    descripcion: Optional[str] = None
    link_imagen: Optional[str] = None
    entrego_premio: Optional[bool] = False
    telefono_invitado: int


@router.put("/")
@limiter.limit("25/minute")
async def asignar_premio_a_invitado(request: Request,
                                    premio_data: PremioAsignacionData,
                                    db: Session = Depends(get_db)):
    """
    Endpoint para asignar un premio a un invitado.
    Actualiza el telefono y la entrega del premio en la tabla premios.
    Actualiza pedido del premio en la tabla invitados.
    """
    # Extrae del JSON
    telefono = premio_data.telefono_invitado
    codigo_premio = premio_data.codigo_premio

    # Verifica si el teléfono existe en la tabla invitados
    invitado = get_invitado(db, telefono)
    if not invitado:
        return {"status": "Error",
                "detail": "Invitado no encontrado para el telefono."}


    # Verifica si el número de teléfono ya está asignado a algún premio
    telefono_existente = (db
                          .query(Premios)
                          .filter(Premios.telefono_invitado == telefono)
                          .first())
    
    if telefono_existente:
        return {"status": "Error",
                "detail": "El teléfono ya está asignado a otro premio."}
    
    # Verifico si el premio ya está asignado a otro invitado
    db_premio = (db
                 .query(Premios)
                 .filter(Premios.codigo_premio == codigo_premio)
                 .first())
    
    if db_premio and db_premio.telefono_invitado:
        return {"status": "Error",
                "detail": "Premio asignado a otro invitado."}

    # Actualiza la información del premio
    premio_dict = {
        'codigo_premio': codigo_premio,
        'telefono_invitado': telefono,
        'entrego_premio': True
    }

    db_premio = update_premio(db, premio_dict)

    # Actualiza el estado del invitado
    invitado.pidio_premio = True
    db.commit()
    db.refresh(invitado)

    return {
        "status": "Premio asignado, datos invitado actualizados",
        "premio": db_premio,
        "invitado": invitado
    }

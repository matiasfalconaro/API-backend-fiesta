from database.crud import (get_db,
                           get_invitado)
from database.models import Invitados
from fastapi import (APIRouter,
                     Depends,
                     Request)
from ..limiter import limiter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional


router = APIRouter()


class InvitadoData(BaseModel):
    """
    Modelo Pydantic (campos opcionales).
    """
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: int
    asiste: Optional[bool] = False
    perfil: Optional[str] = None
    email: Optional[str] = None
    restriccion_alimentaria: Optional[str] = None
    pidio_premio: Optional[bool] = False


@router.put("/")
@limiter.limit("25/minute")
async def create_or_update_invitado(request: Request,
                                    invitado_data: InvitadoData,
                                    db: Session = Depends(get_db)):
    """
    Insertar o actualizar un invitado.
    No sobrescribir campos ya existentes si no hay cambios.
    """
    db_invitado = get_invitado(db, invitado_data.telefono)

    if db_invitado:
        # Verifica preexistencia de los datos
        cambios_realizados = False

        if db_invitado.nombre is None and invitado_data.nombre:
            db_invitado.nombre = invitado_data.nombre
            cambios_realizados = True
        if db_invitado.apellido is None and invitado_data.apellido:
            db_invitado.apellido = invitado_data.apellido
            cambios_realizados = True
        if invitado_data.asiste is not None and db_invitado.asiste != invitado_data.asiste:
            db_invitado.asiste = invitado_data.asiste
            cambios_realizados = True
        if db_invitado.perfil is None and invitado_data.perfil:
            db_invitado.perfil = invitado_data.perfil
            cambios_realizados = True
        if db_invitado.email is None and invitado_data.email:
            db_invitado.email = invitado_data.email
            cambios_realizados = True
        if (db_invitado.restriccion_alimentaria is None
            and invitado_data.restriccion_alimentaria):
            db_invitado.restriccion_alimentaria = invitado_data.restriccion_alimentaria
            cambios_realizados = True
        if invitado_data.pidio_premio is not None and db_invitado.pidio_premio != invitado_data.pidio_premio:
            db_invitado.pidio_premio = invitado_data.pidio_premio
            cambios_realizados = True

        if cambios_realizados:
            db.commit()
            db.refresh(db_invitado)
            return {"status": "Invitado actualizado",
                    "invitado": db_invitado}
        else:
            # No se realizaron cambios
            return {"status": "Invitado ya estaba actualizado",
                    "invitado": db_invitado}

    else:
        # Crea invitado si no existe
        new_invitado = Invitados(
            nombre=invitado_data.nombre,
            apellido=invitado_data.apellido,
            telefono=invitado_data.telefono,
            asiste=invitado_data.asiste,
            perfil=invitado_data.perfil,
            email=invitado_data.email,
            restriccion_alimentaria=invitado_data.restriccion_alimentaria,
            pidio_premio=invitado_data.pidio_premio,
        )
        db.add(new_invitado)
        db.commit()
        db.refresh(new_invitado)
        return {"status": "Invitado creado",
                "invitado": new_invitado}

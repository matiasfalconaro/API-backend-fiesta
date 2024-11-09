from database.crud import get_db
from database.models import Base
from database.session import engine
from fastapi import (APIRouter,
                     Depends,
                     Request)
from ..limiter import limiter
from sqlalchemy.orm import Session


router = APIRouter()


@router.post("/")
@limiter.limit("1/minute")
def reset_database(request: Request,
                   db: Session = Depends(get_db)):
    """
    Resetea la base de datos eliminando todas las tablas y recreándolas.
    """
    Base.metadata.drop_all(bind=engine)  # Elimina todas las tablas
    Base.metadata.create_all(bind=engine)  # Crea todas las tablas nuevamente
    return {"detail": "Base de datos reseteada exitosamente."}

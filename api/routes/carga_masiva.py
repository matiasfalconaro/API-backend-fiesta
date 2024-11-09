import pandas as pd

from database.crud import (bulk_insert_invitados,
                           bulk_insert_premios,
                           get_db)
from fastapi import (APIRouter,
                     File,
                     UploadFile,
                     Depends,
                     HTTPException,
                     Request)
from ..limiter import limiter    
from sqlalchemy.orm import Session
from tempfile import NamedTemporaryFile


router = APIRouter()


@router.post("/")
@limiter.limit("1/minute")
async def upload_excel(request: Request,
                       file: UploadFile = File(...),
                       db: Session = Depends(get_db)):
    """
    Carga masiva de datos preexistentes desde archivo .xlsx
    """
    try:
        # Guardar archivo en un archivo temporal
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name

        df_invitados = pd.read_excel(temp_file_path,
                                     sheet_name='invitados')
        df_premios = pd.read_excel(temp_file_path,
                                   sheet_name='premios')

        # Inseción de datos en DB
        bulk_insert_invitados(db, df_invitados)
        bulk_insert_premios(db, df_premios)

        return {"status": "success",
                "message": "Datos cargados exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400,
                            detail=f"Error al procesar el archivo: {str(e)}")


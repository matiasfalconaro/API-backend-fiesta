import pandas as pd

from database import session
from fastapi import HTTPException
from sqlalchemy.orm import Session
from .models import Invitados, Premios


def get_db():
    """
    Sesión de la DB.
    """
    db = session.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_invitado(db: Session, telefono: int):
    """
    Busca invitado por telefono.
    """
    return (db
            .query(Invitados)
            .filter(Invitados.telefono == telefono)
            .first())


def get_premio(db: Session, telefono_invitado: int):
    """
    Busca invitado por telefono.
    """
    return (db
            .query(Premios)
            .filter(Premios.telefono_invitado == telefono_invitado)
            .first())


def get_all_invitados(db: Session):
    """
    Obtiene todos los invitados de la base de datos.
    """
    return db.query(Invitados).all()


def get_all_premios(db: Session):
    """
    Obtiene todos los invitados de la base de datos.
    """
    return db.query(Premios).all()


def update_invitado(db: Session, invitado_data: dict):
    """
    Actualiza datos del invitado antes de la fiesta.
    """
    db_invitado = get_invitado(db, invitado_data['telefono'])
    if not db_invitado:
        raise HTTPException(status_code=404, detail="Invitado no encontrado")

    # Actualiza campos presentes en JSON y son None
    for campo, valor in invitado_data.items():
        if valor is not None:
            setattr(db_invitado, campo, valor)

    db.commit()
    db.refresh(db_invitado)
    return db_invitado


def update_premio(db: Session, premio_data: dict):
    """
    Actualiza datos del invitado y asigna premio despues de la fiesta.
    """
    # Busca premio segun código_premio
    db_premio = (db.query(Premios)
                 .filter(Premios.codigo_premio == premio_data['codigo_premio'])
                 .first()
    )

    if not db_premio:
        raise HTTPException(status_code=404,
                            detail="Codigo de premio con error")

    # Actualiza campos presentes en JSON
    for campo, valor in premio_data.items():
        if campo in ['premio', 'descripcion', 'link_imagen', 'entrego_premio']:
            # Actualiza directo si están en el dict
            setattr(db_premio, campo, valor)

    # Actualiza teléfono_invitado
    if 'telefono_invitado' in premio_data:
        db_premio.telefono_invitado = premio_data['telefono_invitado']

    db.commit()
    db.refresh(db_premio)
    return db_premio


def bulk_insert_invitados(db: Session, df: pd.DataFrame):
    """
    Función para cargar invitados desde un df.
    """
    required_columns = ['nombre',
                        'apellido',
                        'telefono',
                        'perfil',
                        'email']

    # Verifica columnas del df
    if not all(col in df.columns for col in required_columns):
        raise ValueError("Error columnas en hoja invitados")

    for _, row in df.iterrows():
        try:
            # Campos opcionales: nan -> None
            asiste = row['asiste'] if pd.notna(row['asiste']) else None
            restriccion_alimentaria = (row['restriccion_alimentaria'] 
                                       if pd.notna(row['restriccion_alimentaria'])
                                       else None
                                       )
            
            pidio_premio = (row['pidio_premio']
                            if pd.notna(row['pidio_premio'])
                            else False)  # Default a False si es nan

            invitado = Invitados(nombre=row['nombre'],
                                 apellido=row['apellido'],
                                 telefono=row['telefono'],
                                 asiste=asiste,  # None allow
                                 perfil=row['perfil'],
                                 email=row['email'],
                                 restriccion_alimentaria=restriccion_alimentaria,  # None allow
                                 pidio_premio=pidio_premio  # Por defecto si es nan
            )
            db.add(invitado)
        except Exception as e:
            raise ValueError(f"Error en fila: {row}. Detalles: {str(e)}")
    db.commit()


def bulk_insert_premios(db: Session, df: pd.DataFrame):
    """
    Función para cargar premios desde un df.
    """
    required_columns = ['codigo_premio',
                        'premio',
                        'descripcion',
                        'link_imagen']

    # Verifica columnas del df
    if not all(col in df.columns for col in required_columns):
        raise ValueError("Error columnas en premios")

    for _, row in df.iterrows():
        try:
            # telefono_invitado: nan -> None
            telefono_invitado = (row['telefono_invitado']
                                 if pd.notna(row.get('telefono_invitado'))
                                 else None)

            # entrega_premio: nan -> None
            entrego_premio = (row['entrego_premio']
                              if pd.notna(row.get('entrego_premio'))
                              else False)

            premio = Premios(codigo_premio=row['codigo_premio'],
                             premio=row['premio'],
                             descripcion=row['descripcion'],
                             link_imagen=row['link_imagen'],
                             entrego_premio=entrego_premio,  # Por defecto si es nan
                             telefono_invitado=telefono_invitado  # Permito None si está vacío
            )
            db.add(premio)
        except Exception as e:
            raise ValueError(f"Error en fila: {row}. Detalles: {str(e)}")
    db.commit()

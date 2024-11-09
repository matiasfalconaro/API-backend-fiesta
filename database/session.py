from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)

# Crea tablas
Base.metadata.create_all(bind=engine)

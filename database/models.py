from sqlalchemy import (Column,
                        Integer,
                        String,
                        ForeignKey,
                        Boolean)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Invitados(Base):
    """
    Modelo de datos para la tabla invitados.
    """
    __tablename__ = "invitados"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    telefono = Column(Integer, unique=True, index=True)
    asiste = Column(Boolean, index=True)
    perfil = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    restriccion_alimentaria = Column(String, index=True)
    pidio_premio = Column(Boolean, index=True, default=False)

    # Relaciona Premios por teléfono
    premios = relationship("Premios",
                           back_populates="invitado",
                           uselist=False)


class Premios(Base):
    """
    Modelo de datos para la tabla premios.
    """
    __tablename__ = "premios"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    codigo_premio = Column(String, index=True)
    premio = Column(String, index=True)
    descripcion = Column(String, index=True)
    link_imagen = Column(String, index=True)
    entrego_premio = Column(Boolean, index=True, default=False)

    # Relaciona invitados por teléfono
    telefono_invitado = Column(Integer,
                               ForeignKey("invitados.telefono",
                                          ondelete="SET NULL"),
                               nullable=True)
    invitado = relationship("Invitados",
                            back_populates="premios")

from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from src.core.database import Base

class RolModel(Base):
    __tablename__ = "rol"
    rol_id = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String(50), unique=True, nullable=False)

class EstadoModel(Base):
    __tablename__ = "estado"
    estado_id = Column(Integer, primary_key=True, index=True)
    nombre_estado = Column(String(50), unique=True, nullable=False)

class UsuarioModel(Base):
    __tablename__ = "usuario"
    usuario_id = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String(100), nullable=False)
    contrasenia = Column(String(255), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    rol_id = Column(Integer, ForeignKey("rol.rol_id"))
    estado_id = Column(Integer, ForeignKey("estado.estado_id"))

class ContactoModel(Base):
    __tablename__ = "contacto"
    contacto_id = Column(Integer, primary_key=True, index=True)
    phone_personal = Column(String(30))
    phone_trabajo = Column(String(30))
    domicilio = Column(String(255))
    usuario_id = Column(Integer, ForeignKey("usuario.usuario_id", ondelete="CASCADE"))

class DireccionModel(Base):
    __tablename__ = "direccion"
    direccion_id = Column(Integer, primary_key=True, index=True)
    direccion_texto = Column(String, nullable=False)
    latitud = Column(Numeric(10, 8))
    longitud = Column(Numeric(11, 8))
    referencia = Column(String(255))
    etiqueta = Column(String(50))
    es_temporal = Column(Boolean, default=False)
    usuario_id = Column(Integer, ForeignKey("usuario.usuario_id", ondelete="CASCADE"))
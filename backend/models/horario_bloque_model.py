from sqlalchemy import Column, Integer, ForeignKey, Table
from database import Base

# Tabla de asociación para la relación muchos a muchos
horario_bloque = Table(
    'horario_bloque',
    Base.metadata,
    Column('horario_id', Integer, ForeignKey('horarios.id'), primary_key=True),
    Column('bloque_id', Integer, ForeignKey('bloques.id'), primary_key=True)
)
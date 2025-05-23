from sqlalchemy import Column, Integer , String
from sqlalchemy.orm import relationship
from database import Base

class Horario(Base):
    __tablename__ = "horarios"
    
    id = Column(Integer, primary_key=True)
    franja = Column(String(50) , nullable=True)
    
    # Relación uno a muchos con Bloques
    bloques = relationship("Bloque", back_populates="horario")
    
    # Relación uno a muchos con Cursos
    cursos = relationship("Curso", back_populates="horario")
    
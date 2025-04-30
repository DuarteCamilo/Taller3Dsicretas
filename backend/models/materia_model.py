from sqlalchemy import Column, String, Integer, ARRAY, Boolean
from sqlalchemy.orm import relationship
from database import Base
    
class Materia(Base):
    __tablename__ = "materias"
    
    id = Column(Integer, primary_key=True)
    codigo = Column(String(50), nullable=False , unique=True)
    nombre = Column(String(100), nullable=False)
    cantidad_horas = Column(Integer, nullable=False)
    requiere_sala_sistemas = Column(Boolean, nullable=False)
    
    # Relación con Curso
    cursos = relationship("Curso", back_populates="materia")

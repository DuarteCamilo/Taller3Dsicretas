from sqlalchemy import Column, String, Integer, ARRAY
from sqlalchemy.orm import relationship
from database import Base

class Docente(Base):
    __tablename__ = "docentes"
    
    id = Column(Integer, primary_key=True)
    cc = Column(Integer, nullable=False, unique=True)
    nombre = Column(String(100), nullable=False)  
    restricciones = Column(ARRAY(String(50)), nullable=True)  
    materias = Column(ARRAY(Integer), nullable=True)  

    # Relación con Curso
    cursos = relationship("Curso", back_populates="docente")
    
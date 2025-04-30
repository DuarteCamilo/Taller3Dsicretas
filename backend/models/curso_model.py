from sqlalchemy import Column, String, Integer, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
    
class Curso(Base):
    __tablename__ = "cursos"
    
    id = Column(Integer, primary_key=True)
    codigo = Column(String(50), nullable=False, unique=True)
    horario_id = Column(Integer, ForeignKey("horarios.id"))
    docente_id = Column(Integer, ForeignKey("docentes.id"))
    grupo = Column(String(50), nullable=False)
    materia_id = Column(Integer, ForeignKey("materias.id"))
    
    # Relación con Horario
    horario = relationship("Horario", back_populates="cursos")

    # Relación con Docente
    docente = relationship("Docente", back_populates="cursos")

    # Relación con Materia
    materia = relationship("Materia", back_populates="cursos")
    
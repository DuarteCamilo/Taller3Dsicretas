from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
    
class Bloque(Base):
    __tablename__ = "bloques"
    
    id = Column(Integer, primary_key=True)
    dia = Column(String(50), nullable=False)
    horaInicio = Column(Integer, nullable=False)  
    horaFin = Column(Integer, nullable=False)     
    salon_id = Column(Integer, ForeignKey("salones.id"), nullable=False)
    horario_id = Column(Integer, ForeignKey("horarios.id"))  # Bloque pertenece a un Horario
    
    # Relación con Horario
    horario = relationship("Horario", back_populates="bloques")
    
    # Relación con Salon
    salon = relationship("Salon", back_populates="bloques")
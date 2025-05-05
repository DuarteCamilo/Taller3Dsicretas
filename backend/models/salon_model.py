from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship
from database import Base
    
class Salon(Base):
    __tablename__ = "salones"
    
    id = Column(Integer, primary_key=True)
    bloque = Column(String(50), nullable=False)
    numero = Column(Integer, nullable=False)
    es_sistemas = Column(Boolean, nullable=False)
      
    # Relación con el modelo Bloque
    bloques = relationship("Bloque", back_populates="salon")
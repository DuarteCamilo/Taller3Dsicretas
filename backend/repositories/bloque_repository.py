from typing import List
from sqlalchemy.orm import Session
from models.bloque_model import Bloque

class BloqueRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, bloque_request):
        """Crea un nuevo bloque en la base de datos."""
        bloque_model = Bloque(**bloque_request)
        self.db.add(bloque_model)
        self.db.commit()
        self.db.refresh(bloque_model)
        return bloque_model
    
    def get_by_id(self, bloque_id: int):
        """Obtiene un bloque por su ID."""
        return self.db.query(Bloque).filter(Bloque.id == bloque_id).first()
    
    def get_all(self):
        """Obtiene todos los bloques."""
        return self.db.query(Bloque).all()
    
    def get_by_dia(self, dia: str):
        """Obtiene bloques por día."""
        return self.db.query(Bloque).filter(Bloque.dia == dia).all()
    
    def get_by_horario(self, horario_id: int):
        """Obtiene bloques por horario."""
        return self.db.query(Bloque).filter(Bloque.horario_id == horario_id).all()
    
    def get_by_salon(self, salon_id: int):
        """Obtiene bloques por salón."""
        return self.db.query(Bloque).filter(Bloque.salon_id == salon_id).all()
    
    def get_by_hora(self, hora_inicio: int, hora_fin: int):
        """Obtiene bloques por rango de horas."""
        return self.db.query(Bloque).filter(
            Bloque.horaInicio >= hora_inicio,
            Bloque.horaFin <= hora_fin
        ).all()
    
    def update(self, bloque_id: int, bloque_data: dict):
        """Actualiza un bloque existente."""
        bloque = self.get_by_id(bloque_id)
        if bloque:
            for key, value in bloque_data.items():
                setattr(bloque, key, value)
            self.db.commit()
            self.db.refresh(bloque)
        return bloque
    
    def delete(self, bloque_id: int):
        """Elimina un bloque por su ID."""
        bloque = self.get_by_id(bloque_id)
        if bloque:
            self.db.delete(bloque)
            self.db.commit()
            return True
        return False

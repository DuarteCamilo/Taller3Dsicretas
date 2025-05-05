from typing import List
from sqlalchemy.orm import Session
from models.salon_model import Salon

class SalonRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, salon_request):
        salon_model = Salon(**salon_request)
        self.db.add(salon_model)
        self.db.commit()
        self.db.refresh(salon_model)
        return salon_model
    
    def get_by_id(self, salon_id: int):
        """Obtiene un salón por su ID."""
        return self.db.query(Salon).filter(Salon.id == salon_id).first()
    
    def get_all(self):
        """Obtiene todos los salones."""
        return self.db.query(Salon).all()
    
    def get_by_bloque(self, bloque: str):
        """Obtiene salones por bloque."""
        return self.db.query(Salon).filter(Salon.bloque == bloque).all()
    
    def update(self, salon_id: int, salon_data: dict):
        """Actualiza un salón existente."""
        salon = self.get_by_id(salon_id)
        if salon:
            for key, value in salon_data.items():
                setattr(salon, key, value)
            self.db.commit()
            self.db.refresh(salon)
        return salon
    
    def delete(self, salon_id: int):
        """Elimina un salón por su ID."""
        salon = self.get_by_id(salon_id)
        if salon:
            self.db.delete(salon)
            self.db.commit()
            return True
        return False



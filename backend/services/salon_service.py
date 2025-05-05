from sqlalchemy.orm import Session
from repositories.salon_repository import SalonRepository
from schemas.requests.salon_request import SalonRequest
from typing import List, Optional

class SalonService:
    def __init__(self, db: Session):
        self.db = db
        self.salon_repository = SalonRepository(db)

    def create_salon(self, salon_request: SalonRequest):
        """Crea un nuevo salón en la base de datos."""
        # Convertir el request a un diccionario para pasarlo al repositorio
        salon_data = salon_request.dict()
        
        # Llamar al repositorio para crear el salón
        new_salon = self.salon_repository.create(salon_data)
        
        return new_salon
    
    def get_salon_by_id(self, salon_id: int):
        """Obtiene un salón por su ID."""
        return self.salon_repository.get_by_id(salon_id)
    
    def get_salones(self):
        """Obtiene todos los salones."""
        return self.salon_repository.get_all()
    
    def get_salones_by_bloque(self, bloque: str):
        """Obtiene salones por bloque."""
        return self.salon_repository.get_by_bloque(bloque)
    
    def update_salon(self, salon_id: int, salon_request: SalonRequest):
        """Actualiza un salón existente."""
        salon_data = salon_request.dict()
        return self.salon_repository.update(salon_id, salon_data)
    
    def delete_salon(self, salon_id: int):
        """Elimina un salón por su ID."""
        return self.salon_repository.delete(salon_id)


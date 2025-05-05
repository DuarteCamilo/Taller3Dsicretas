from sqlalchemy.orm import Session
from repositories.salon_repository import SalonRepository
from schemas.requests.salon_request import SalonRequest
from schemas.responses.salon_response import SalonResponse
from typing import List, Optional

class SalonService:
    def __init__(self, db: Session):
        self.db = db
        self.salon_repository = SalonRepository(db)
    
    def to_salon_response(self, salon):
        """Método auxiliar para crear un objeto SalonResponse a partir de un objeto salón."""
        return SalonResponse(
            id=salon.id,
            bloque=salon.bloque,
            numero=salon.numero,
            es_sistemas=salon.es_sistemas
        )

    def create_salon(self, salon_request: SalonRequest):
        """Crea un nuevo salón en la base de datos."""
        # Convertir el request a un diccionario para pasarlo al repositorio
        salon_data = salon_request.dict()
        
        # Llamar al repositorio para crear el salón
        new_salon = self.salon_repository.create(salon_data)
        
        # Crear y retornar el objeto SalonResponse
        return self.to_salon_response(new_salon)
    
    def get_salon_by_id(self, salon_id: int):
        """Obtiene un salón por su ID."""
        salon = self.salon_repository.get_by_id(salon_id)
        if not salon:
            return None
            
        return self.to_salon_response(salon)
    
    def get_salones(self):
        """Obtiene todos los salones."""
        salones = self.salon_repository.get_all()
        
        return [self.to_salon_response(salon) for salon in salones]
    
    def get_salones_by_bloque(self, bloque: str):
        """Obtiene salones por bloque."""
        salones = self.salon_repository.get_by_bloque(bloque)
        
        return [self.to_salon_response(salon) for salon in salones]
    
    def update_salon(self, salon_id: int, salon_request: SalonRequest):
        """Actualiza un salón existente."""
        salon_data = salon_request.dict()
        salon = self.salon_repository.update(salon_id, salon_data)
        
        if not salon:
            return None
            
        return self.to_salon_response(salon)
    
    def delete_salon(self, salon_id: int):
        """Elimina un salón por su ID."""
        return self.salon_repository.delete(salon_id)


from sqlalchemy.orm import Session
from repositories.materia_repository import MateriaRepository
from schemas.requests.materia_request import MateriaRequest
from typing import List, Optional

class MateriaService:
    def __init__(self, db: Session):
        self.db = db
        self.materia_repository = MateriaRepository(db)

    def create_materia(self, materia_request: MateriaRequest):
        """Crea una nueva materia en la base de datos."""
        # Convertir el request a un diccionario para pasarlo al repositorio
        materia_data = materia_request.dict()
        
        # Llamar al repositorio para crear la materia
        new_materia = self.materia_repository.create(materia_data)
        
        return new_materia
    
    def get_materia_by_id(self, materia_id: int):
        """Obtiene una materia por su ID."""
        return self.materia_repository.get_by_id(materia_id)
    
    def get_materias(self):
        """Obtiene todas las materias."""
        return self.materia_repository.get_all()
    
    def get_materia_by_codigo(self, codigo: str):
        """Obtiene una materia por su código."""
        return self.materia_repository.get_by_codigo(codigo)
    
    def get_materias_by_nombre(self, nombre: str):
        """Obtiene materias por nombre."""
        return self.materia_repository.get_by_nombre(nombre)
    
    def get_materias_by_sistemas(self, requiere_sistemas: bool):
        """Obtiene materias que requieren o no sala de sistemas."""
        return self.materia_repository.get_by_sistemas(requiere_sistemas)
    
    def update_materia(self, materia_id: int, materia_request: MateriaRequest):
        """Actualiza una materia existente."""
        materia_data = materia_request.dict()
        return self.materia_repository.update(materia_id, materia_data)
    
    def delete_materia(self, materia_id: int):
        """Elimina una materia por su ID."""
        return self.materia_repository.delete(materia_id)
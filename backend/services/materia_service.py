from sqlalchemy.orm import Session
from repositories.materia_repository import MateriaRepository
from schemas.requests.materia_request import MateriaRequest
from schemas.responses.materia_response import MateriaResponse
from typing import List, Optional

class MateriaService:
    def __init__(self, db: Session):
        self.db = db
        self.materia_repository = MateriaRepository(db)

    def to_materia_response(self, materia):
        """Método auxiliar para crear un objeto MateriaResponse a partir de un objeto materia."""
        return MateriaResponse(
            id=materia.id,
            codigo=materia.codigo,
            nombre=materia.nombre,
            cantidad_horas=materia.cantidad_horas,
            requiere_sala_sistemas=materia.requiere_sala_sistemas
        )

    def create_materia(self, materia_request: MateriaRequest):
        """Crea una nueva materia en la base de datos."""
        # Convertir el request a un diccionario para pasarlo al repositorio
        materia_data = materia_request.dict()
        
        # Llamar al repositorio para crear la materia
        new_materia = self.materia_repository.create(materia_data)
        
        # Crear y retornar el objeto MateriaResponse
        return self.to_materia_response(new_materia)
    
    def get_materia_by_id(self, materia_id: int):
        """Obtiene una materia por su ID."""
        materia = self.materia_repository.get_by_id(materia_id)
        if not materia:
            return None
        
        return self.to_materia_response(materia)
    
    def get_materias(self):
        """Obtiene todas las materias."""
        materias = self.materia_repository.get_all()
        
        return [self.to_materia_response(materia) for materia in materias]
    
    def get_materia_by_codigo(self, codigo: str):
        """Obtiene una materia por su código."""
        materia = self.materia_repository.get_by_codigo(codigo)
        if not materia:
            return None
            
        return self.to_materia_response(materia)
    
    def get_materias_by_nombre(self, nombre: str):
        """Obtiene materias por nombre."""
        materias = self.materia_repository.get_by_nombre(nombre)
        
        return [self.to_materia_response(materia) for materia in materias]
    
    def get_materias_by_sistemas(self, requiere_sistemas: bool):
        """Obtiene materias que requieren o no sala de sistemas."""
        materias = self.materia_repository.get_by_sistemas(requiere_sistemas)
        
        return [self.to_materia_response(materia) for materia in materias]
    
    def update_materia(self, materia_id: int, materia_request: MateriaRequest):
        """Actualiza una materia existente."""
        materia_data = materia_request.dict()
        materia = self.materia_repository.update(materia_id, materia_data)
        
        if not materia:
            return None
            
        return self.to_materia_response(materia)
    
    def delete_materia(self, materia_id: int):
        """Elimina una materia por su ID."""
        return self.materia_repository.delete(materia_id)
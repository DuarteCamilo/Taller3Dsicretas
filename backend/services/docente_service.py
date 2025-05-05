from sqlalchemy.orm import Session
from repositories.docente_repository import DocenteRepository
from schemas.requests.docente_request import DocenteRequest
from typing import List, Optional

class DocenteService:
    def __init__(self, db: Session):
        self.db = db
        self.docente_repository = DocenteRepository(db)

    def create_docente(self, docente_request: DocenteRequest):
        """Crea un nuevo docente en la base de datos."""
        # Convertir el request a un diccionario para pasarlo al repositorio
        docente_data = docente_request.dict()
        
        # Llamar al repositorio para crear el docente
        new_docente = self.docente_repository.create(docente_data)
        
        return new_docente
    
    def get_docente_by_id(self, docente_id: int):
        """Obtiene un docente por su ID."""
        return self.docente_repository.get_by_id(docente_id)
    
    def get_docente_by_cc(self, cc: int):
        """Obtiene un docente por su número de cédula."""
        return self.docente_repository.get_by_cc(cc)
    
    def get_docentes(self):
        """Obtiene todos los docentes."""
        return self.docente_repository.get_all()
    
    def update_docente(self, docente_id: int, docente_request: DocenteRequest):
        """Actualiza un docente existente."""
        docente_data = docente_request.dict()
        return self.docente_repository.update(docente_id, docente_data)
    
    def delete_docente(self, docente_id: int):
        """Elimina un docente por su ID."""
        return self.docente_repository.delete(docente_id)
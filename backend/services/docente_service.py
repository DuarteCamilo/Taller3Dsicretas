from sqlalchemy.orm import Session
from repositories.docente_repository import DocenteRepository
from schemas.requests.docente_request import DocenteRequest
from schemas.responses.docente_response import DocenteResponse
from typing import List, Optional

class DocenteService:
    def __init__(self, db: Session):
        self.db = db
        self.docente_repository = DocenteRepository(db)

    def to_docente_response(self, docente):
        """Método auxiliar para crear un objeto DocenteResponse a partir de un objeto docente."""
        return DocenteResponse(
            id=docente.id,
            cc=docente.cc,
            nombre=docente.nombre,
            restricciones=docente.restricciones,
            materias=docente.materias
        )

    def create_docente(self, docente_request: DocenteRequest):
        """Crea un nuevo docente en la base de datos """
        # Convertir el request a un diccionario para pasarlo al repositorio
        docente_data = docente_request.dict()
        
        # Llamar al repositorio para crear el docente
        new_docente = self.docente_repository.create(docente_data)
        
        # Crear y retornar el objeto DocenteResponse
        return self.to_docente_response(new_docente)
    
    def get_docente_by_id(self, docente_id: int):
        """Obtiene un docente por su ID y retorna un DocenteResponse."""
        docente = self.docente_repository.get_by_id(docente_id)
        if not docente:
            return None
        
        return self.to_docente_response(docente)
    
    def get_docente_by_cc(self, cc: int):
        """Obtiene un docente por su número de cédula y retorna un DocenteResponse."""
        docente = self.docente_repository.get_by_cc(cc)
        if not docente:
            return None
        
        return self.to_docente_response(docente)
    
    def get_docentes(self):
        """Obtiene todos los docentes y retorna una lista de DocenteResponse."""
        docentes = self.docente_repository.get_all()
        
        return [self.to_docente_response(docente) for docente in docentes]
    
    def update_docente(self, docente_id: int, docente_request: DocenteRequest):
        """Actualiza un docente existente y retorna un DocenteResponse."""
        docente_data = docente_request.dict()
        docente = self.docente_repository.update(docente_id, docente_data)
        
        if not docente:
            return None
        
        return self.to_docente_response(docente)
    
    def delete_docente(self, docente_id: int):
        """Elimina un docente por su ID."""
        return self.docente_repository.delete(docente_id)
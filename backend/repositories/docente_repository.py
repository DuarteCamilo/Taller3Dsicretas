from typing import List
from sqlalchemy.orm import Session
from models.docente_model import Docente

class DocenteRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, docente_request):
        """Crea un nuevo docente en la base de datos."""
        docente_model = Docente(**docente_request)
        self.db.add(docente_model)
        self.db.commit()
        self.db.refresh(docente_model)
        return docente_model
    
    def get_by_id(self, docente_id: int):
        """Obtiene un docente por su ID."""
        return self.db.query(Docente).filter(Docente.id == docente_id).first()
    
    def get_by_cc(self, cc: int):
        """Obtiene un docente por su número de cédula."""
        return self.db.query(Docente).filter(Docente.cc == cc).first()
    
    def get_all(self):
        """Obtiene todos los docentes."""
        return self.db.query(Docente).all()
    
    def update(self, docente_id: int, docente_data: dict):
        """Actualiza un docente existente."""
        docente = self.get_by_id(docente_id)
        if docente:
            for key, value in docente_data.items():
                setattr(docente, key, value)
            self.db.commit()
            self.db.refresh(docente)
        return docente
    
    def delete(self, docente_id: int):
        """Elimina un docente por su ID."""
        docente = self.get_by_id(docente_id)
        if docente:
            self.db.delete(docente)
            self.db.commit()
            return True
        return False
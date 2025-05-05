from typing import List
from sqlalchemy.orm import Session
from models.materia_model import Materia

class MateriaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, materia_request):
        materia_model = Materia(**materia_request)
        self.db.add(materia_model)
        self.db.commit()
        self.db.refresh(materia_model)
        return materia_model
    
    def get_by_id(self, materia_id: int):
        """Obtiene una materia por su ID."""
        return self.db.query(Materia).filter(Materia.id == materia_id).first()
    
    def get_all(self):
        """Obtiene todas las materias."""
        return self.db.query(Materia).all()
    
    def get_by_codigo(self, codigo: str):
        """Obtiene materias por código."""
        return self.db.query(Materia).filter(Materia.codigo == codigo).first()
    
    def get_by_nombre(self, nombre: str):
        """Obtiene materias por nombre."""
        return self.db.query(Materia).filter(Materia.nombre.ilike(f"%{nombre}%")).all()
    
    def get_by_sistemas(self, requiere_sistemas: bool):
        """Obtiene materias que requieren o no sala de sistemas."""
        return self.db.query(Materia).filter(Materia.requiere_sala_sistemas == requiere_sistemas).all()
    
    def update(self, materia_id: int, materia_data: dict):
        """Actualiza una materia existente."""
        materia = self.get_by_id(materia_id)
        if materia:
            for key, value in materia_data.items():
                setattr(materia, key, value)
            self.db.commit()
            self.db.refresh(materia)
        return materia
    
    def delete(self, materia_id: int):
        """Elimina una materia por su ID."""
        materia = self.get_by_id(materia_id)
        if materia:
            self.db.delete(materia)
            self.db.commit()
            return True
        return False
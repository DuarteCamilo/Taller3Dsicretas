from typing import List
from sqlalchemy.orm import Session
from models.horario_model import Horario

class HorarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, horario_request):
        """Crea un nuevo horario en la base de datos."""
        horario_model = Horario(**horario_request)
        self.db.add(horario_model)
        self.db.commit()
        self.db.refresh(horario_model)
        return horario_model
    
    def get_by_id(self, horario_id: int):
        """Obtiene un horario por su ID."""
        return self.db.query(Horario).filter(Horario.id == horario_id).first()
    
    def get_all(self):
        """Obtiene todos los horarios."""
        return self.db.query(Horario).all()
    
    def get_by_curso(self, curso_id: int):
        """Obtiene horarios por curso."""
        return self.db.query(Horario).join(Horario.cursos).filter(Curso.id == curso_id).all()
    
    def get_by_bloque(self, bloque_id: int):
        """Obtiene horarios por bloque."""
        return self.db.query(Horario).join(Horario.bloques).filter(Bloque.id == bloque_id).all()
    
    def update(self, horario_id: int, horario_data: dict):
        """Actualiza un horario existente."""
        horario = self.get_by_id(horario_id)
        if horario:
            for key, value in horario_data.items():
                setattr(horario, key, value)
            self.db.commit()
            self.db.refresh(horario)
        return horario
    
    def delete(self, horario_id: int):
        """Elimina un horario por su ID."""
        horario = self.get_by_id(horario_id)
        if horario:
            self.db.delete(horario)
            self.db.commit()
            return True
        return False
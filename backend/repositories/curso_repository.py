from typing import List
from sqlalchemy.orm import Session , joinedload
from models.horario_model import Horario
from models.curso_model import Curso


class CursoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, curso_request):
        """Crea un nuevo curso en la base de datos."""
        curso_model = Curso(**curso_request)
        self.db.add(curso_model)
        self.db.commit()
        self.db.refresh(curso_model)
        return curso_model
    
    def get_by_id(self, curso_id: int):
        """Obtiene un curso por su ID."""
        return self.db.query(Curso).filter(Curso.id == curso_id).first()
    
    def get_all(self):
        """Obtiene todos los cursos."""
        return self.db.query(Curso).all()
    
    def get_all_with_relations(self):
        """Obtiene todos los cursos con sus relaciones cargadas."""
        return self.db.query(Curso).options(
            joinedload(Curso.docente),
            joinedload(Curso.horario).joinedload(Horario.bloques),
            joinedload(Curso.materia)
        ).all()
    
    def get_by_id_with_relations(self, curso_id: int):
        """Obtiene un curso por su ID con todas sus relaciones cargadas."""
        return self.db.query(Curso).options(
            joinedload(Curso.docente),
            joinedload(Curso.horario).joinedload(Horario.bloques),
            joinedload(Curso.materia)
        ).filter(Curso.id == curso_id).first()
    
    def get_by_codigo(self, codigo: str):
        """Obtiene un curso por su código."""
        return self.db.query(Curso).filter(Curso.codigo == codigo).first()
    
    def get_by_docente(self, docente_id: int):
        """Obtiene cursos por docente."""
        return self.db.query(Curso).filter(Curso.docente_id == docente_id).all()
    
    def get_by_materia(self, materia_id: int):
        """Obtiene cursos por materia."""
        return self.db.query(Curso).filter(Curso.materia_id == materia_id).all()
    
    def get_by_grupo(self, grupo: str):
        """Obtiene cursos por grupo."""
        return self.db.query(Curso).filter(Curso.grupo.ilike(f"%{grupo}%")).all()
    
    def update(self, curso_id: int, curso_data: dict):
        """Actualiza un curso existente."""
        curso = self.get_by_id(curso_id)
        if curso:
            for key, value in curso_data.items():
                setattr(curso, key, value)
            self.db.commit()
            self.db.refresh(curso)
        return curso
    
    def delete(self, curso_id: int):
        """Elimina un curso por su ID."""
        curso = self.get_by_id(curso_id)
        if curso:
            self.db.delete(curso)
            self.db.commit()
            return True
        return False
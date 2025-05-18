from sqlalchemy.orm import Session
from typing import List

from repositories.curso_repository import CursoRepository
from repositories.docente_repository import DocenteRepository
from repositories.horario_repository import HorarioRepository
from repositories.materia_repository import MateriaRepository
from repositories.bloque_repository import BloqueRepository
from repositories.salon_repository import SalonRepository

from schemas.responses.curso_response import CursoResponse, CursoResponse2
from schemas.responses.docente_response import DocenteResponse
from schemas.responses.horario_response import HorarioResponse
from schemas.responses.materia_response import MateriaResponse
from schemas.responses.bloque_response import BloqueResponse
from schemas.responses.salon_response import SalonResponse

class CursoService:
    def __init__(self, db: Session):
        self.db = db
        self.curso_repository = CursoRepository(db)
        self.docente_repository = DocenteRepository(db)
        self.horario_repository = HorarioRepository(db)
        self.materia_repository = MateriaRepository(db)
        self.bloque_repository = BloqueRepository(db)
        self.salon_repository = SalonRepository(db)
    
    def to_curso_response(self, curso):
        """Convierte un modelo de curso a un objeto CursoResponse."""
        return CursoResponse(
            id=curso.id,
            codigo=curso.codigo,
            horario_id=curso.horario_id,
            docente_id=curso.docente_id,
            grupo=curso.grupo,
            materia_id=curso.materia_id
        )
    
    def to_curso_response2(self, curso):
        """Convierte un modelo de curso a un objeto CursoResponse2 con todas las relaciones."""
        # Obtener bloques del horario
        bloques = self.bloque_repository.get_by_horario(curso.horario_id)
        bloques_response = []
        
        for bloque in bloques:
            # Obtener información del salón para cada bloque
            salon = self.salon_repository.get_by_id(bloque.salon_id)
            salon_response = SalonResponse(
                id=salon.id,
                bloque=salon.bloque,
                numero=salon.numero,
                es_sistemas=salon.es_sistemas
            )
            
            # Crear respuesta de bloque con salón incluido
            bloque_response = BloqueResponse(
                id=bloque.id,
                dia=bloque.dia,
                horaInicio=bloque.horaInicio,
                horaFin=bloque.horaFin,
                salon_id=bloque.salon_id,
                horario_id=bloque.horario_id,
                salon=salon_response
            )
            bloques_response.append(bloque_response)
        
        # Crear respuesta de horario con bloques completos
        horario_response = HorarioResponse(
            id=curso.horario.id,
            franja=curso.horario.franja,
            bloques=bloques_response
        )
        
        # Crear respuesta de docente
        docente_response = DocenteResponse(
            id=curso.docente.id,
            cc=curso.docente.cc,
            nombre=curso.docente.nombre,
            restricciones=curso.docente.restricciones,
            materias=curso.docente.materias
        )
        
        # Crear respuesta de materia
        materia_response = MateriaResponse(
            id=curso.materia.id,
            codigo=curso.materia.codigo,
            nombre=curso.materia.nombre,
            cantidad_horas=curso.materia.cantidad_horas,
            requiere_sala_sistemas=curso.materia.requiere_sala_sistemas
        )
        
        # Crear respuesta completa del curso
        return CursoResponse2(
            id=curso.id,
            codigo=curso.codigo,
            grupo=curso.grupo,
            docente=docente_response,
            horario=horario_response,
            materia=materia_response
        )
    
    def get_all_cursos(self):
        """Obtiene todos los cursos en formato básico."""
        cursos = self.curso_repository.get_all()
        return [self.to_curso_response(curso) for curso in cursos]
    
    def get_all_cursos_with_details(self):
        """Obtiene todos los cursos con información completa."""
        cursos = self.curso_repository.get_all_with_relations()
        return [self.to_curso_response2(curso) for curso in cursos]
    
    def get_curso_by_id_with_details(self, curso_id: int):
        """Obtiene un curso específico con información completa."""
        curso = self.curso_repository.get_by_id_with_relations(curso_id)
        if not curso:
            return None
        return self.to_curso_response2(curso)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from services.curso_service import CursoService
from schemas.responses.curso_response import CursoResponse, CursoResponse2

router = APIRouter(tags=["cursos"])

@router.get("/", response_model=List[CursoResponse])
def get_all_cursos(db: Session = Depends(get_db)):
    """
    Obtiene todos los cursos en formato básico.
    
    Returns:
        List[CursoResponse]: Lista de cursos con información básica
    """
    service = CursoService(db)
    return service.get_all_cursos()

@router.get("/detallados", response_model=List[CursoResponse2])
def get_all_cursos_detallados(db: Session = Depends(get_db)):
    """
    Obtiene todos los cursos con información completa incluyendo docente, horario y materia.
    
    Returns:
        List[CursoResponse2]: Lista de cursos con información detallada
    """
    service = CursoService(db)
    return service.get_all_cursos_with_details()

@router.get("/{curso_id}", response_model=CursoResponse)
def get_curso_by_id(curso_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un curso específico por su ID en formato básico.
    
    Args:
        curso_id (int): ID del curso a buscar
        
    Returns:
        CursoResponse: Información básica del curso
    """
    service = CursoService(db)
    curso = service.curso_repository.get_by_id(curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return service.to_curso_response(curso)

@router.get("/{curso_id}/detallado", response_model=CursoResponse2)
def get_curso_by_id_detallado(curso_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un curso específico por su ID con información completa.
    
    Args:
        curso_id (int): ID del curso a buscar
        
    Returns:
        CursoResponse2: Información detallada del curso
    """
    service = CursoService(db)
    curso = service.get_curso_by_id_with_details(curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso
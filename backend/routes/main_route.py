from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.main_service import MainService

router = APIRouter(tags=["main"])

@router.post("/generar-horarios")
def generar_horarios_automaticos(db: Session = Depends(get_db)):
    """
    Endpoint para generar automáticamente los horarios de cursos.
    
    Este endpoint ejecuta el algoritmo de generación de horarios que:
    - Crea cursos basados en docentes, materias y salones disponibles
    - Asigna bloques de horario según las reglas establecidas
    - Respeta las restricciones de docentes y requisitos de materias
    
    Returns:
        Dict: Resultado de la generación con información de éxito y detalles
    """
    service = MainService(db)
    resultado = service.generar_horarios_automaticos()
    
    if not resultado["exito"]:
        raise HTTPException(status_code=400, detail=resultado["mensaje"])
    
    return resultado

@router.delete("/limpiar-horarios")
def limpiar_horarios(db: Session = Depends(get_db)):
    """
    Endpoint para limpiar todos los horarios, bloques y cursos generados.
    
    Útil para reiniciar el sistema antes de una nueva generación de horarios.
    
    Returns:
        Dict: Resultado de la operación con información de éxito y detalles
    """
    service = MainService(db)
    resultado = service.limpiar_horarios()
    
    if not resultado["exito"]:
        raise HTTPException(status_code=400, detail=resultado["mensaje"])
    
    return resultado
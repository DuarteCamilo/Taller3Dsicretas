from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, Path, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas.requests.materia_request import MateriaRequest
from schemas.responses.materia_response import MateriaResponse
from services.materia_service import MateriaService


router = APIRouter(tags=["materias"])

@router.post("/create", response_model=MateriaResponse)
async def create_materia(
    materia_request: MateriaRequest,
    db: Session = Depends(get_db)
):
    # Inicializar servicio
    materia_service = MateriaService(db)
    
    try:
        # Llamar al servicio para crear la materia
        return materia_service.create_materia(materia_request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get-materias", response_model=List[MateriaResponse])
async def get_materias(
    db: Session = Depends(get_db)
):
    materia_service = MateriaService(db)
    return materia_service.get_materias()

@router.get("/by-codigo/{codigo}", response_model=MateriaResponse)
async def get_materia_by_codigo(
    codigo: str = Path(..., description="Código de la materia a obtener"),
    db: Session = Depends(get_db)
):
    materia_service = MateriaService(db)
    materia = materia_service.get_materia_by_codigo(codigo)
    
    if not materia:
        raise HTTPException(status_code=404, detail=f"Materia con código {codigo} no encontrada")
    
    return materia

@router.get("/by-nombre", response_model=List[MateriaResponse])
async def get_materias_by_nombre(
    nombre: Optional[str] = Query(None, description="Filtrar por nombre"),
    db: Session = Depends(get_db)
):
    materia_service = MateriaService(db)
    return materia_service.get_materias_by_nombre(nombre)

@router.get("/by-sistemas", response_model=List[MateriaResponse])
async def get_materias_by_sistemas(
    requiere_sistemas: bool = Query(..., description="Filtrar por requerimiento de sala de sistemas"),
    db: Session = Depends(get_db)
):
    materia_service = MateriaService(db)
    return materia_service.get_materias_by_sistemas(requiere_sistemas)

@router.get("/get-by-id/{materia_id}", response_model=MateriaResponse)
async def get_materia_by_id(
    materia_id: int = Path(..., description="ID de la materia a obtener"),
    db: Session = Depends(get_db)
):
    materia_service = MateriaService(db)
    materia = materia_service.get_materia_by_id(materia_id)
    
    if not materia:
        raise HTTPException(status_code=404, detail=f"Materia con ID {materia_id} no encontrada")
    
    return materia

@router.put("/update/{materia_id}", response_model=MateriaResponse)
async def update_materia(
    materia_id: int = Path(..., description="ID de la materia a actualizar"),
    materia_request: MateriaRequest = None,
    db: Session = Depends(get_db)
):
    materia_service = MateriaService(db)
    materia = materia_service.update_materia(materia_id, materia_request)
    
    if not materia:
        raise HTTPException(status_code=404, detail=f"Materia con ID {materia_id} no encontrada")
    
    return materia

@router.delete("/delete/{materia_id}", response_model=dict)
async def delete_materia(
    materia_id: int = Path(..., description="ID de la materia a eliminar"),
    db: Session = Depends(get_db)
):
    materia_service = MateriaService(db)
    success = materia_service.delete_materia(materia_id)
    
    if not success:
        raise HTTPException(status_code=404, detail=f"Materia con ID {materia_id} no encontrada")
    
    return {"message": f"Materia con ID {materia_id} eliminada correctamente"}
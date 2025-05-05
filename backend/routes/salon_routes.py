from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, Path, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas.requests.salon_request import SalonRequest
from schemas.responses.salon_response import SalonResponse
from services.salon_service import SalonService


router = APIRouter(tags=["salones"])

@router.post("/create", response_model=SalonResponse)
async def create_salon(
    salon_request: SalonRequest,
    db: Session = Depends(get_db)
):
    # Inicializar servicio
    salon_service = SalonService(db)
    
    try:
        # Llamar al servicio para crear el salón
        return salon_service.create_salon(salon_request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get-salones", response_model=List[SalonResponse])
async def get_salones(
    db: Session = Depends(get_db)
):
    salon_service = SalonService(db)
    return salon_service.get_salones()

@router.get("/by-bloque", response_model=List[SalonResponse])
async def get_salones_by_bloque(
    bloque: Optional[str] = Query(None, description="Filtrar por bloque"),
    db: Session = Depends(get_db)
):
    salon_service = SalonService(db)
    return salon_service.get_salones_by_bloque(bloque)

@router.get("/get-by-id/{salon_id}", response_model=SalonResponse)
async def get_salon_by_id(
    salon_id: int = Path(..., description="ID del salón a obtener"),
    db: Session = Depends(get_db)
):
    salon_service = SalonService(db)
    salon = salon_service.get_salon_by_id(salon_id)
    
    if not salon:
        raise HTTPException(status_code=404, detail=f"Salón con ID {salon_id} no encontrado")
    
    return salon

@router.put("/update/{salon_id}", response_model=SalonResponse)
async def update_salon(
    salon_id: int = Path(..., description="ID del salón a actualizar"),
    salon_request: SalonRequest = None,
    db: Session = Depends(get_db)
):
    salon_service = SalonService(db)
    salon = salon_service.update_salon(salon_id, salon_request)
    
    if not salon:
        raise HTTPException(status_code=404, detail=f"Salón con ID {salon_id} no encontrado")
    
    return salon

@router.delete("/delete/{salon_id}", response_model=dict)
async def delete_salon(
    salon_id: int = Path(..., description="ID del salón a eliminar"),
    db: Session = Depends(get_db)
):
    salon_service = SalonService(db)
    success = salon_service.delete_salon(salon_id)
    
    if not success:
        raise HTTPException(status_code=404, detail=f"Salón con ID {salon_id} no encontrado")
    
    return {"message": f"Salón con ID {salon_id} eliminado correctamente"}
   
  
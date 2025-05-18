from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas.requests.docente_request import DocenteRequest
from schemas.responses.docente_response import DocenteResponse, DocenteResponse2
from services.docente_service import DocenteService

router = APIRouter(tags=["docentes"])

@router.post("/create", response_model=DocenteResponse)
async def create_docente(
    docente_request: DocenteRequest,
    db: Session = Depends(get_db)
):
    # Inicializar servicio
    docente_service = DocenteService(db)
    
    try:
        # Llamar al servicio para crear el docente y obtener la respuesta
        return docente_service.create_docente(docente_request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/get-docentes", response_model=List[DocenteResponse2])
async def get_docentes(
    db: Session = Depends(get_db)
):
    docente_service = DocenteService(db)
    return docente_service.get_docentes_with_materias()

@router.get("/get-by-id/{docente_id}", response_model=DocenteResponse2)
async def get_docente_by_id(
    docente_id: int = Path(..., description="ID del docente a obtener"),
    db: Session = Depends(get_db)
):
    docente_service = DocenteService(db)
    docente = docente_service.get_docente_by_id_with_materias(docente_id)
    
    if not docente:
        raise HTTPException(status_code=404, detail=f"Docente con ID {docente_id} no encontrado")
    
    return docente

@router.get("/get-by-cc/{cc}", response_model=DocenteResponse2)
async def get_docente_by_cc(
    cc: int = Path(..., description="Cédula del docente a obtener"),
    db: Session = Depends(get_db)
):
    docente_service = DocenteService(db)
    docente = docente_service.get_docente_by_cc_with_materias(cc)
    
    if not docente:
        raise HTTPException(status_code=404, detail=f"Docente con cédula {cc} no encontrado")
    
    return docente

@router.put("/update/{docente_id}", response_model=DocenteResponse)
async def update_docente(
    docente_id: int = Path(..., description="ID del docente a actualizar"),
    docente_request: DocenteRequest = None,
    db: Session = Depends(get_db)
):
    docente_service = DocenteService(db)
    docente = docente_service.update_docente(docente_id, docente_request)
    
    if not docente:
        raise HTTPException(status_code=404, detail=f"Docente con ID {docente_id} no encontrado")
    
    return docente

@router.delete("/delete/{docente_id}", response_model=dict)
async def delete_docente(
    docente_id: int = Path(..., description="ID del docente a eliminar"),
    db: Session = Depends(get_db)
):
    docente_service = DocenteService(db)
    success = docente_service.delete_docente(docente_id)
    
    if not success:
        raise HTTPException(status_code=404, detail=f"Docente con ID {docente_id} no encontrado")
    
    return {"message": f"Docente con ID {docente_id} eliminado correctamente"}
from pydantic import BaseModel
from typing import List, Optional
from schemas.responses.materia_response import MateriaResponse

class DocenteResponse(BaseModel):
    id: int
    cc: int
    nombre: str
    restricciones: Optional[List[str]] = None
    materias: Optional[List[int]] = None
    
class DocenteResponse2(BaseModel):
    id: int
    cc: int
    nombre: str
    restricciones: Optional[List[str]] = None
    materias: Optional[List[MateriaResponse]] = None
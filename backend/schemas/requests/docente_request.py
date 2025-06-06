from pydantic import BaseModel
from typing import List, Optional

class DocenteRequest(BaseModel):
    cc: int
    nombre: str
    restricciones: Optional[List[str]] = None
    materias: Optional[List[int]] = None
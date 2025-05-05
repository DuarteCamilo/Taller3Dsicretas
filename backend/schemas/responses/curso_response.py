from pydantic import BaseModel
from typing import Optional

class CursoResponse(BaseModel):
    id: int
    codigo: str
    horario_id: int
    docente_id: int
    grupo: str
    materia_id: int
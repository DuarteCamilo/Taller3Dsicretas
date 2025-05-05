from pydantic import BaseModel
from typing import Optional

class CursoRequest(BaseModel):
    codigo: str
    horario_id: int
    docente_id: int
    grupo: str
    materia_id: int
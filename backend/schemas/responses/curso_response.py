from pydantic import BaseModel
from typing import Optional, List
from schemas.responses.docente_response import DocenteResponse
from schemas.responses.horario_response import HorarioResponse
from schemas.responses.materia_response import MateriaResponse
from schemas.responses.bloque_response import BloqueResponse

class CursoResponse(BaseModel):
    id: int
    codigo: str
    horario_id: int
    docente_id: int
    grupo: str
    materia_id: int

class CursoResponse2(BaseModel):
    id: int
    codigo: str
    grupo: str
    docente: DocenteResponse
    horario: HorarioResponse
    materia: MateriaResponse
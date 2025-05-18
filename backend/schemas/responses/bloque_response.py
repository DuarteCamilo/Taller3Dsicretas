from pydantic import BaseModel
from typing import Optional
from schemas.responses.salon_response import SalonResponse

class BloqueResponse(BaseModel):
    id: int
    dia: str
    horaInicio: int
    horaFin: int    
    horario_id: int
    salon: SalonResponse
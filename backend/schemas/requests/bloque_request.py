from pydantic import BaseModel

class BloqueRequest(BaseModel):
    dia: str
    horaInicio: int
    horaFin: int    
    salon_id: int
    horario_id: int
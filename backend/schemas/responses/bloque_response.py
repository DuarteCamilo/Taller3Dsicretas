from pydantic import BaseModel
class BloqueResponse(BaseModel):
    id: int
    dia: str
    horaInicio: int
    horaFin: int    
    salon_id: int
    horario_id: int
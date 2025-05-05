from pydantic import BaseModel

class HorarioBloqueRequest(BaseModel):
    horario_id: int
    bloque_id: int
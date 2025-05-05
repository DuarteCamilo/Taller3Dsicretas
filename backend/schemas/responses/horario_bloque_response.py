from pydantic import BaseModel

class HorarioBloqueResponse(BaseModel):
    horario_id: int
    bloque_id: int
from pydantic import BaseModel
from typing import List, Optional
from schemas.responses.bloque_response import BloqueResponse

class HorarioResponse(BaseModel):
    id: int
    franja: str
    # Agregamos el campo bloques para incluir la información completa
    bloques: Optional[List[BloqueResponse]] = None

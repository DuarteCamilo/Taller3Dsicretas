from pydantic import BaseModel
from typing import List, Optional

class HorarioResponse(BaseModel):
    id: int
    franja: str
    # Opcionalmente, podríamos incluir listas de IDs de bloques y cursos relacionados
    bloques_ids: Optional[List[int]] = None
    cursos_ids: Optional[List[int]] = None
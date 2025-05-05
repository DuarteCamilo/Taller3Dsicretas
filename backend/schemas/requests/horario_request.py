from pydantic import BaseModel
from typing import List, Optional

class HorarioRequest(BaseModel):
    # El modelo Horario solo tiene un ID como atributo propio
    # Los demás atributos son relaciones
    pass
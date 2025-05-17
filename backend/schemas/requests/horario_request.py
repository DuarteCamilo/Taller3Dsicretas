from pydantic import BaseModel
from typing import List, Optional

class HorarioRequest(BaseModel):
    franja: str
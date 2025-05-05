from pydantic import BaseModel

class SalonRequest(BaseModel):
    bloque: str
    numero: int
    es_sistemas: bool
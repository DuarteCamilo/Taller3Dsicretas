from pydantic import BaseModel


class SalonResponse(BaseModel):
    id: int
    bloque: str
    numero: int
    es_sistemas: bool
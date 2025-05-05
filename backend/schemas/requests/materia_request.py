from pydantic import BaseModel

class MateriaRequest(BaseModel):
    codigo: str
    nombre: str
    cantidad_horas: int
    requiere_sala_sistemas: bool
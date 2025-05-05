from pydantic import BaseModel


class MateriaResponse(BaseModel):
    id: int
    codigo: str
    nombre: str
    cantidad_horas: int
    requiere_sala_sistemas: bool
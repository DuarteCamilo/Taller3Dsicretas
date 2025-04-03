from fastapi import APIRouter
from services.message_service import get_message

router = APIRouter(
    prefix="/api",
    tags=["messages"]
)

@router.get("/message")
def read_message():
    """
    Endpoint simple que retorna un mensaje
    """
    return {"message": get_message()}
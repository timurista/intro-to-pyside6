from fastapi import APIRouter
from ..models import User
from ..services import AuthService

router = APIRouter()

@router.post("/login")
async def login(user: User):
    return AuthService.login(user)

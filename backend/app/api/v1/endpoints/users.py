from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.schemas.api import UserResponse
from app.models.user import User

router = APIRouter()

@router.get("/me", response_model=UserResponse, summary="Get current logged-in user info")
async def get_me(current_user: User = Depends(get_current_user)):
    """Returns profile information for the authenticated user."""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        created_at=current_user.created_at
    )

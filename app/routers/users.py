from fastapi import APIRouter, Depends
from typing import Annotated
from app.dependencies.auth import get_current_active_user
from app.models.user import User
from app.schemas.user import UserProfile

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserProfile)
def get_user_profile(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    Get the current authenticated user's profile
    
    Requires authentication via JWT token
    
    Returns the user's profile information
    """
    return current_user

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated
from app.database import get_db
from app.models.user import User, UserRole
from app.utils.security import decode_access_token
from app.utils.exceptions import UnauthorizedException, ForbiddenException

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)]
) -> User:
    """
    Dependency to get the current authenticated user from JWT token
    
    Args:
        token: JWT token from Authorization header
        db: Database session
        
    Returns:
        Current authenticated user
        
    Raises:
        UnauthorizedException: If token is invalid or user not found
    """
    # Decode token
    payload = decode_access_token(token)
    if payload is None:
        raise UnauthorizedException(detail="Could not validate credentials")
    
    # Extract email from token
    email: str = payload.get("sub")
    if email is None:
        raise UnauthorizedException(detail="Could not validate credentials")
    
    # Get user from database
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise UnauthorizedException(detail="User not found")
    
    return user


def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """
    Dependency to ensure the current user is active
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Current active user
        
    Raises:
        ForbiddenException: If user is inactive
    """
    if not current_user.is_active:
        raise ForbiddenException(detail="Inactive user")
    
    return current_user


def require_role(required_role: UserRole):
    """
    Factory function to create a dependency that requires a specific role
    
    Args:
        required_role: The role required to access the endpoint
        
    Returns:
        Dependency function that checks user role
    """
    def role_checker(current_user: Annotated[User, Depends(get_current_active_user)]) -> User:
        if current_user.role != required_role:
            raise ForbiddenException(
                detail=f"This endpoint requires {required_role.value} role"
            )
        return current_user
    
    return role_checker


# Convenience dependencies for common roles
require_student = require_role(UserRole.STUDENT)
require_admin = require_role(UserRole.ADMIN)

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from app.database import get_db
from app.schemas.auth import UserRegister, Token
from app.schemas.user import UserResponse
from app.models.user import User
from app.utils.security import hash_password, verify_password, create_access_token
from app.utils.exceptions import BadRequestException, UnauthorizedException

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserRegister,
    db: Annotated[Session, Depends(get_db)]
):
    """
    Register a new user
    
    - **name**: User's full name (2-100 characters)
    - **email**: Valid email address (must be unique)
    - **password**: Password (minimum 6 characters)
    - **role**: User role (student or admin, defaults to student)
    
    Returns the created user information (excluding password)
    """
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise BadRequestException(detail="Email already registered")
    
    # Create new user
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role=user_data.role,
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=Token)
def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Login and receive a JWT access token
    
    - **username**: User's email address
    - **password**: User's password
    
    Returns an access token for authentication
    """
    # Find user by email (OAuth2PasswordRequestForm uses 'username' field)
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # Verify user exists and password is correct
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise UnauthorizedException(detail="Incorrect email or password")
    
    # Check if user is active
    if not user.is_active:
        raise UnauthorizedException(detail="Inactive user account")
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}

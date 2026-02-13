from pydantic import BaseModel, EmailStr, ConfigDict
from app.models.user import UserRole


class UserBase(BaseModel):
    """Base user schema"""
    name: str
    email: EmailStr
    role: UserRole


class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)


class UserProfile(UserResponse):
    """Schema for authenticated user profile"""
    pass

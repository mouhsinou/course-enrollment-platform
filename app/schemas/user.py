from pydantic import BaseModel, EmailStr, ConfigDict
from app.models.user import UserRole
from typing import List, Optional
# Forward reference to avoid circular import if needed, but we can import directly if no cycle
# But wait, schemas/enrollment.py doesn't import user.py.
# However, user.py is used by auth.py, etc.
# Let's use TYPE_CHECKING or just import if no cycle.
from app.schemas.enrollment import EnrollmentResponse


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


    
    model_config = ConfigDict(from_attributes=True)


class UserProfile(UserResponse):
    """Schema for authenticated user profile"""
    enrollments: List[EnrollmentResponse] = []

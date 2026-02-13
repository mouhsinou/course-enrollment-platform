from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class EnrollmentCreate(BaseModel):
    """Schema for creating an enrollment"""
    course_id: int


class EnrollmentUserInfo(BaseModel):
    """Schema for user info in enrollment response"""
    id: int
    name: str
    email: str
    
    model_config = ConfigDict(from_attributes=True)


class EnrollmentCourseInfo(BaseModel):
    """Schema for course info in enrollment response"""
    id: int
    title: str
    code: str
    
    model_config = ConfigDict(from_attributes=True)


class EnrollmentResponse(BaseModel):
    """Schema for enrollment response"""
    id: int
    user_id: int
    course_id: int
    created_at: datetime
    user: Optional[EnrollmentUserInfo] = None
    course: Optional[EnrollmentCourseInfo] = None
    
    model_config = ConfigDict(from_attributes=True)


class EnrollmentList(BaseModel):
    """Schema for list of enrollments"""
    enrollments: list[EnrollmentResponse]
    total: int

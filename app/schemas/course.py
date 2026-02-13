from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional


class CourseBase(BaseModel):
    """Base course schema"""
    title: str = Field(..., min_length=3, max_length=200)
    code: str = Field(..., min_length=2, max_length=50)
    capacity: int = Field(..., gt=0)
    
    @field_validator('code')
    @classmethod
    def validate_code(cls, v):
        if not v.strip():
            raise ValueError('Code cannot be empty or whitespace')
        return v.strip().upper()
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip()


class CourseCreate(CourseBase):
    """Schema for creating a course"""
    is_active: bool = True


class CourseUpdate(BaseModel):
    """Schema for updating a course"""
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    code: Optional[str] = Field(None, min_length=2, max_length=50)
    capacity: Optional[int] = Field(None, gt=0)
    is_active: Optional[bool] = None
    
    @field_validator('code')
    @classmethod
    def validate_code(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Code cannot be empty or whitespace')
        return v.strip().upper() if v else v
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip() if v else v


class CourseResponse(CourseBase):
    """Schema for course response"""
    id: int
    is_active: bool
    enrolled_count: int = 0
    available_slots: int = 0
    
    model_config = ConfigDict(from_attributes=True)

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated, List
from app.database import get_db
from app.dependencies.auth import get_current_active_user, require_admin
from app.models.user import User
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse
from app.utils.exceptions import NotFoundException, BadRequestException

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("", response_model=List[CourseResponse])
def get_all_active_courses(
    db: Annotated[Session, Depends(get_db)]
):
    """
    Get all active courses (public endpoint)
    
    Returns a list of all active courses with enrollment information
    """
    courses = db.query(Course).filter(Course.is_active == True).all()
    return courses


@router.get("/{course_id}", response_model=CourseResponse)
def get_course_by_id(
    course_id: int,
    db: Annotated[Session, Depends(get_db)]
):
    """
    Get a specific course by ID (public endpoint)
    
    Returns course details with enrollment information
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise NotFoundException(detail="Course not found")
    
    return course


@router.post("", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(
    course_data: CourseCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_admin)]
):
    """
    Create a new course (admin only)
    
    - **title**: Course title (3-200 characters)
    - **code**: Unique course code (2-50 characters, will be converted to uppercase)
    - **capacity**: Maximum number of students (must be > 0)
    - **is_active**: Whether the course is active (defaults to true)
    
    Returns the created course
    """
    # Check if course code already exists
    existing_course = db.query(Course).filter(Course.code == course_data.code).first()
    if existing_course:
        raise BadRequestException(detail=f"Course with code '{course_data.code}' already exists")
    
    # Create new course
    new_course = Course(
        title=course_data.title,
        code=course_data.code,
        capacity=course_data.capacity,
        is_active=course_data.is_active
    )
    
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    
    return new_course


@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    course_data: CourseUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_admin)]
):
    """
    Update a course (admin only)
    
    All fields are optional. Only provided fields will be updated.
    
    - **title**: Course title (3-200 characters)
    - **code**: Unique course code (2-50 characters, will be converted to uppercase)
    - **capacity**: Maximum number of students (must be > 0)
    - **is_active**: Whether the course is active
    
    Returns the updated course
    """
    # Get course
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise NotFoundException(detail="Course not found")
    
    # Check if new code conflicts with existing course
    if course_data.code and course_data.code != course.code:
        existing_course = db.query(Course).filter(Course.code == course_data.code).first()
        if existing_course:
            raise BadRequestException(detail=f"Course with code '{course_data.code}' already exists")
    
    # Update fields
    update_data = course_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(course, field, value)
    
    db.commit()
    db.refresh(course)
    
    return course


@router.patch("/{course_id}/activate", response_model=CourseResponse)
def toggle_course_activation(
    course_id: int,
    is_active: bool,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_admin)]
):
    """
    Activate or deactivate a course (admin only)
    
    - **is_active**: True to activate, False to deactivate
    
    Returns the updated course
    """
    # Get course
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise NotFoundException(detail="Course not found")
    
    # Update activation status
    course.is_active = is_active
    
    db.commit()
    db.refresh(course)
    
    return course

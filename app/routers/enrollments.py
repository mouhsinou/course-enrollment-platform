from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated, List
from app.database import get_db
from app.dependencies.auth import get_current_active_user, require_admin
from app.models.user import User, UserRole
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse, EnrollmentList
from app.utils.exceptions import NotFoundException, BadRequestException, ForbiddenException

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


@router.post("", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def enroll_in_course(
    enrollment_data: EnrollmentCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    Enroll the current user in a course (student only)
    
    - **course_id**: ID of the course to enroll in
    
    Business rules:
    - Only students can enroll
    - Cannot enroll in the same course twice
    - Course must be active
    - Course must not be full
    
    Returns the created enrollment
    """
    # Only students can enroll
    if current_user.role != UserRole.STUDENT:
        raise ForbiddenException(detail="Only students can enroll in courses")
    
    # Check if course exists
    course = db.query(Course).filter(Course.id == enrollment_data.course_id).first()
    if not course:
        raise NotFoundException(detail="Course not found")
    
    # Check if course is active
    if not course.is_active:
        raise BadRequestException(detail="Cannot enroll in inactive course")
    
    # Check if already enrolled
    existing_enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id,
        Enrollment.course_id == enrollment_data.course_id
    ).first()
    if existing_enrollment:
        raise BadRequestException(detail="Already enrolled in this course")
    
    # Check if course is full
    if course.is_full:
        raise BadRequestException(detail="Course is full")
    
    # Create enrollment
    new_enrollment = Enrollment(
        user_id=current_user.id,
        course_id=enrollment_data.course_id
    )
    
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    
    return new_enrollment


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def deregister_from_course(
    course_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    Deregister the current user from a course (student only)
    
    - **course_id**: ID of the course to deregister from
    
    Returns 204 No Content on success
    """
    # Only students can deregister
    if current_user.role != UserRole.STUDENT:
        raise ForbiddenException(detail="Only students can deregister from courses")
    
    # Find enrollment
    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id,
        Enrollment.course_id == course_id
    ).first()
    
    if not enrollment:
        raise NotFoundException(detail="Enrollment not found")
    
    # Delete enrollment
    db.delete(enrollment)
    db.commit()
    
    return None


@router.get("", response_model=List[EnrollmentResponse])
def get_all_enrollments(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_admin)]
):
    """
    Get all enrollments (admin only)
    
    Returns a list of all enrollments with user and course details
    """
    enrollments = db.query(Enrollment).all()
    return enrollments


@router.get("/course/{course_id}", response_model=List[EnrollmentResponse])
def get_course_enrollments(
    course_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_admin)]
):
    """
    Get all enrollments for a specific course (admin only)
    
    - **course_id**: ID of the course
    
    Returns a list of enrollments for the specified course
    """
    # Check if course exists
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise NotFoundException(detail="Course not found")
    
    # Get enrollments
    enrollments = db.query(Enrollment).filter(Enrollment.course_id == course_id).all()
    return enrollments


@router.delete("/{enrollment_id}/admin", status_code=status.HTTP_204_NO_CONTENT)
def remove_student_from_course(
    enrollment_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(require_admin)]
):
    """
    Remove a student from a course (admin only)
    
    - **enrollment_id**: ID of the enrollment to remove
    
    Returns 204 No Content on success
    """
    # Find enrollment
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise NotFoundException(detail="Enrollment not found")
    
    # Delete enrollment
    db.delete(enrollment)
    db.commit()
    
    return None

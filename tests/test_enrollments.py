import pytest
from fastapi import status
from app.models.enrollment import Enrollment


class TestEnrollInCourse:
    """Test student enrollment endpoint"""
    
    def test_enroll_success(self, client, student_token, sample_course):
        """Test successful enrollment"""
        response = client.post(
            "/enrollments",
            json={"course_id": sample_course.id},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["course_id"] == sample_course.id
        assert "created_at" in data
    
    def test_enroll_duplicate(self, client, student_token, sample_course, db_session, student_user):
        """Test enrolling in the same course twice"""
        # First enrollment
        enrollment = Enrollment(user_id=student_user.id, course_id=sample_course.id)
        db_session.add(enrollment)
        db_session.commit()
        
        # Try to enroll again
        response = client.post(
            "/enrollments",
            json={"course_id": sample_course.id},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already enrolled" in response.json()["detail"].lower()
    
    def test_enroll_in_inactive_course(self, client, student_token, inactive_course):
        """Test enrolling in an inactive course"""
        response = client.post(
            "/enrollments",
            json={"course_id": inactive_course.id},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "inactive" in response.json()["detail"].lower()
    
    def test_enroll_in_full_course(self, client, db_session):
        """Test enrolling in a full course"""
        # Create a new student
        from app.models.user import User, UserRole
        from app.utils.security import hash_password, create_access_token
        
        new_student = User(
            name="New Student",
            email="newstudent@test.com",
            hashed_password=hash_password("password123"),
            role=UserRole.STUDENT,
            is_active=True
        )
        db_session.add(new_student)
        db_session.commit()
        db_session.refresh(new_student)
        
        new_token = create_access_token(data={"sub": new_student.email})
        
        # Create a full course
        from app.models.course import Course
        course = Course(title="Full Course", code="FULL101", capacity=1, is_active=True)
        db_session.add(course)
        db_session.commit()
        db_session.refresh(course)
        
        # Fill the course
        enrollment = Enrollment(user_id=new_student.id, course_id=course.id)
        db_session.add(enrollment)
        db_session.commit()
        
        # Create another student
        another_student = User(
            name="Another Student",
            email="another@test.com",
            hashed_password=hash_password("password123"),
            role=UserRole.STUDENT,
            is_active=True
        )
        db_session.add(another_student)
        db_session.commit()
        
        another_token = create_access_token(data={"sub": another_student.email})
        
        # Try to enroll in full course
        response = client.post(
            "/enrollments",
            json={"course_id": course.id},
            headers={"Authorization": f"Bearer {another_token}"}
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "full" in response.json()["detail"].lower()
    
    def test_enroll_nonexistent_course(self, client, student_token):
        """Test enrolling in a non-existent course"""
        response = client.post(
            "/enrollments",
            json={"course_id": 9999},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_enroll_as_admin(self, client, admin_token, sample_course):
        """Test admin trying to enroll (should fail)"""
        response = client.post(
            "/enrollments",
            json={"course_id": sample_course.id},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_enroll_no_auth(self, client, sample_course):
        """Test enrolling without authentication"""
        response = client.post(
            "/enrollments",
            json={"course_id": sample_course.id}
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestDeregisterFromCourse:
    """Test student deregistration endpoint"""
    
    def test_deregister_success(self, client, student_token, sample_course, db_session, student_user):
        """Test successful deregistration"""
        # First enroll
        enrollment = Enrollment(user_id=student_user.id, course_id=sample_course.id)
        db_session.add(enrollment)
        db_session.commit()
        
        # Then deregister
        response = client.delete(
            f"/enrollments/{sample_course.id}",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_deregister_not_enrolled(self, client, student_token, sample_course):
        """Test deregistering from a course not enrolled in"""
        response = client.delete(
            f"/enrollments/{sample_course.id}",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_deregister_as_admin(self, client, admin_token, sample_course):
        """Test admin trying to deregister (should fail)"""
        response = client.delete(
            f"/enrollments/{sample_course.id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestAdminEnrollmentManagement:
    """Test admin enrollment management endpoints"""
    
    def test_get_all_enrollments(self, client, admin_token, db_session, student_user, sample_course):
        """Test admin getting all enrollments"""
        # Create some enrollments
        enrollment = Enrollment(user_id=student_user.id, course_id=sample_course.id)
        db_session.add(enrollment)
        db_session.commit()
        
        response = client.get(
            "/enrollments",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 1
    
    def test_get_all_enrollments_as_student(self, client, student_token):
        """Test student trying to get all enrollments (should fail)"""
        response = client.get(
            "/enrollments",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_course_enrollments(self, client, admin_token, db_session, student_user, sample_course):
        """Test admin getting enrollments for a specific course"""
        # Create enrollment
        enrollment = Enrollment(user_id=student_user.id, course_id=sample_course.id)
        db_session.add(enrollment)
        db_session.commit()
        
        response = client.get(
            f"/enrollments/course/{sample_course.id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["course_id"] == sample_course.id
    
    def test_get_course_enrollments_nonexistent_course(self, client, admin_token):
        """Test getting enrollments for non-existent course"""
        response = client.get(
            "/enrollments/course/9999",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_remove_student_from_course(self, client, admin_token, db_session, student_user, sample_course):
        """Test admin removing a student from a course"""
        # Create enrollment
        enrollment = Enrollment(user_id=student_user.id, course_id=sample_course.id)
        db_session.add(enrollment)
        db_session.commit()
        db_session.refresh(enrollment)
        
        response = client.delete(
            f"/enrollments/{enrollment.id}/admin",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_remove_student_as_student(self, client, student_token, db_session, student_user, sample_course):
        """Test student trying to use admin removal endpoint (should fail)"""
        # Create enrollment
        enrollment = Enrollment(user_id=student_user.id, course_id=sample_course.id)
        db_session.add(enrollment)
        db_session.commit()
        db_session.refresh(enrollment)
        
        response = client.delete(
            f"/enrollments/{enrollment.id}/admin",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

import pytest
from fastapi import status


class TestGetCourses:
    """Test course retrieval endpoints"""
    
    def test_get_all_active_courses(self, client, sample_course, inactive_course):
        """Test getting all active courses"""
        response = client.get("/courses")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["code"] == sample_course.code
        assert data[0]["is_active"] is True
    
    def test_get_course_by_id(self, client, sample_course):
        """Test getting a specific course by ID"""
        response = client.get(f"/courses/{sample_course.id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == sample_course.id
        assert data["code"] == sample_course.code
        assert data["title"] == sample_course.title
    
    def test_get_nonexistent_course(self, client):
        """Test getting a non-existent course"""
        response = client.get("/courses/9999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestCreateCourse:
    """Test course creation endpoint"""
    
    def test_create_course_as_admin(self, client, admin_token):
        """Test creating a course as admin"""
        response = client.post(
            "/courses",
            json={
                "title": "Web Development",
                "code": "web101",
                "capacity": 25,
                "is_active": True
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["code"] == "WEB101"  # Should be uppercase
        assert data["title"] == "Web Development"
        assert data["capacity"] == 25
    
    def test_create_course_as_student(self, client, student_token):
        """Test creating a course as student (should fail)"""
        response = client.post(
            "/courses",
            json={
                "title": "Web Development",
                "code": "WEB101",
                "capacity": 25
            },
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_create_course_duplicate_code(self, client, admin_token, sample_course):
        """Test creating a course with duplicate code"""
        response = client.post(
            "/courses",
            json={
                "title": "Another Course",
                "code": sample_course.code,
                "capacity": 20
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_create_course_invalid_capacity(self, client, admin_token):
        """Test creating a course with invalid capacity"""
        response = client.post(
            "/courses",
            json={
                "title": "Invalid Course",
                "code": "INV101",
                "capacity": 0
            },
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_course_no_auth(self, client):
        """Test creating a course without authentication"""
        response = client.post(
            "/courses",
            json={
                "title": "Web Development",
                "code": "WEB101",
                "capacity": 25
            }
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestUpdateCourse:
    """Test course update endpoint"""
    
    def test_update_course_as_admin(self, client, admin_token, sample_course):
        """Test updating a course as admin"""
        response = client.put(
            f"/courses/{sample_course.id}",
            json={"title": "Updated Title", "capacity": 40},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["capacity"] == 40
        assert data["code"] == sample_course.code  # Unchanged
    
    def test_update_course_as_student(self, client, student_token, sample_course):
        """Test updating a course as student (should fail)"""
        response = client.put(
            f"/courses/{sample_course.id}",
            json={"title": "Updated Title"},
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_update_nonexistent_course(self, client, admin_token):
        """Test updating a non-existent course"""
        response = client.put(
            "/courses/9999",
            json={"title": "Updated Title"},
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestToggleCourseActivation:
    """Test course activation toggle endpoint"""
    
    def test_deactivate_course(self, client, admin_token, sample_course):
        """Test deactivating a course"""
        response = client.patch(
            f"/courses/{sample_course.id}/activate?is_active=false",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["is_active"] is False
    
    def test_activate_course(self, client, admin_token, inactive_course):
        """Test activating a course"""
        response = client.patch(
            f"/courses/{inactive_course.id}/activate?is_active=true",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["is_active"] is True
    
    def test_toggle_activation_as_student(self, client, student_token, sample_course):
        """Test toggling activation as student (should fail)"""
        response = client.patch(
            f"/courses/{sample_course.id}/activate?is_active=false",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

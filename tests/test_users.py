import pytest
from fastapi import status


class TestUserProfile:
    """Test user profile endpoint"""
    
    def test_get_profile_success(self, client, student_user, student_token):
        """Test getting user profile with valid token"""
        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == student_user.email
        assert data["name"] == student_user.name
        assert data["role"] == student_user.role.value
    
    def test_get_profile_no_token(self, client):
        """Test getting profile without token"""
        response = client.get("/users/me")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_profile_invalid_token(self, client):
        """Test getting profile with invalid token"""
        response = client.get(
            "/users/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

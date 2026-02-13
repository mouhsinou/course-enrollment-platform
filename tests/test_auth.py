import pytest
from fastapi import status


class TestUserRegistration:
    """Test user registration endpoint"""
    
    def test_register_student_success(self, client):
        """Test successful student registration"""
        response = client.post("/auth/register", json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
            "role": "student"
        })
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == "john@example.com"
        assert data["name"] == "John Doe"
        assert data["role"] == "student"
        assert data["is_active"] is True
        assert "hashed_password" not in data
    
    def test_register_admin_success(self, client):
        """Test successful admin registration"""
        response = client.post("/auth/register", json={
            "name": "Admin User",
            "email": "admin@example.com",
            "password": "password123",
            "role": "admin"
        })
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["role"] == "admin"
    
    def test_register_duplicate_email(self, client, student_user):
        """Test registration with duplicate email"""
        response = client.post("/auth/register", json={
            "name": "Another User",
            "email": student_user.email,
            "password": "password123",
            "role": "student"
        })
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already registered" in response.json()["detail"].lower()
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email"""
        response = client.post("/auth/register", json={
            "name": "Test User",
            "email": "invalid-email",
            "password": "password123",
            "role": "student"
        })
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_short_password(self, client):
        """Test registration with short password"""
        response = client.post("/auth/register", json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "123",
            "role": "student"
        })
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_empty_name(self, client):
        """Test registration with empty name"""
        response = client.post("/auth/register", json={
            "name": "   ",
            "email": "test@example.com",
            "password": "password123",
            "role": "student"
        })
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestUserLogin:
    """Test user login endpoint"""
    
    def test_login_success(self, client, student_user):
        """Test successful login"""
        response = client.post("/auth/login", data={
            "username": student_user.email,
            "password": "password123"
        })
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_wrong_password(self, client, student_user):
        """Test login with wrong password"""
        response = client.post("/auth/login", data={
            "username": student_user.email,
            "password": "wrongpassword"
        })
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        response = client.post("/auth/login", data={
            "username": "nonexistent@example.com",
            "password": "password123"
        })
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_login_inactive_user(self, client, inactive_user):
        """Test login with inactive user"""
        response = client.post("/auth/login", data={
            "username": inactive_user.email,
            "password": "password123"
        })
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "inactive" in response.json()["detail"].lower()

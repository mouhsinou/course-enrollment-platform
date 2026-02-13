import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.database import Base, get_db
from app.models.user import User, UserRole
from app.models.course import Course
from app.utils.security import hash_password, create_access_token

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def student_user(db_session):
    """Create a test student user"""
    user = User(
        name="Test Student",
        email="student@test.com",
        hashed_password=hash_password("password123"),
        role=UserRole.STUDENT,
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def admin_user(db_session):
    """Create a test admin user"""
    user = User(
        name="Test Admin",
        email="admin@test.com",
        hashed_password=hash_password("password123"),
        role=UserRole.ADMIN,
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def inactive_user(db_session):
    """Create an inactive test user"""
    user = User(
        name="Inactive User",
        email="inactive@test.com",
        hashed_password=hash_password("password123"),
        role=UserRole.STUDENT,
        is_active=False
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def student_token(student_user):
    """Create a JWT token for the student user"""
    return create_access_token(data={"sub": student_user.email})


@pytest.fixture
def admin_token(admin_user):
    """Create a JWT token for the admin user"""
    return create_access_token(data={"sub": admin_user.email})


@pytest.fixture
def sample_course(db_session):
    """Create a sample active course"""
    course = Course(
        title="Introduction to Python",
        code="CS101",
        capacity=30,
        is_active=True
    )
    db_session.add(course)
    db_session.commit()
    db_session.refresh(course)
    return course


@pytest.fixture
def inactive_course(db_session):
    """Create an inactive course"""
    course = Course(
        title="Advanced Algorithms",
        code="CS401",
        capacity=20,
        is_active=False
    )
    db_session.add(course)
    db_session.commit()
    db_session.refresh(course)
    return course


@pytest.fixture
def full_course(db_session, student_user):
    """Create a course that is full"""
    from app.models.enrollment import Enrollment
    
    course = Course(
        title="Database Systems",
        code="CS301",
        capacity=1,
        is_active=True
    )
    db_session.add(course)
    db_session.commit()
    db_session.refresh(course)
    
    # Fill the course
    enrollment = Enrollment(user_id=student_user.id, course_id=course.id)
    db_session.add(enrollment)
    db_session.commit()
    
    return course

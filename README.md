# Course Enrollment Platform API

A secure, database-backed RESTful API built with FastAPI for managing a course enrollment platform with authentication, authorization, and comprehensive business rules.

## 🚀 Features

- **JWT Authentication**: Secure user authentication with JSON Web Tokens
- **Role-Based Access Control (RBAC)**: Student and Admin roles with different permissions
- **Course Management**: Create, update, and manage courses with capacity tracking
- **Enrollment System**: Students can enroll/deregister with business rule validation
- **Database Migrations**: Version-controlled database schema with Alembic
- **Comprehensive Testing**: Full test coverage for all endpoints and business logic
- **API Documentation**: Auto-generated interactive API docs with Swagger UI

## 📋 Requirements

- Python 3.10+
- PostgreSQL 12+ (or SQLite for development)
- pip (Python package manager)

## 🛠️ Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Alembic**: Database migration tool
- **PostgreSQL**: Production database
- **Pydantic**: Data validation using Python type annotations
- **JWT**: JSON Web Tokens for authentication
- **Pytest**: Testing framework
- **Bcrypt**: Password hashing

## 📁 Project Structure

```
altschool/
├── app/
│   ├── models/          # SQLAlchemy database models
│   ├── schemas/         # Pydantic schemas for validation
│   ├── routers/         # API route handlers
│   ├── dependencies/    # Dependency injection (auth, etc.)
│   ├── utils/           # Utility functions (security, exceptions)
│   ├── config.py        # Configuration settings
│   ├── database.py      # Database connection
│   └── main.py          # FastAPI application
├── tests/               # Test suite
├── alembic/             # Database migrations
├── requirements.txt     # Python dependencies
└── README.md
```

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
cd altschool
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/course_enrollment
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
```

**For SQLite (development only):**
```env
DATABASE_URL=sqlite:///./course_enrollment.db
```

### 5. Set Up PostgreSQL Database

```bash
# Create database
createdb course_enrollment

# Or using psql
psql -U postgres
CREATE DATABASE course_enrollment;
```

## 📊 Database Migrations

### Initialize Alembic (already done)

```bash
alembic init alembic
```

### Create Initial Migration

```bash
alembic revision --autogenerate -m "Initial migration: users, courses, enrollments"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migration

```bash
alembic downgrade -1
```

## 🚀 Running the Application

### Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Production Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🧪 Running Tests

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=term-missing
```

### Run Specific Test File

```bash
pytest tests/test_auth.py -v
```

### Run Specific Test Class

```bash
pytest tests/test_enrollments.py::TestEnrollInCourse -v
```

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register` | Register a new user | No |
| POST | `/auth/login` | Login and get JWT token | No |

### User Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/users/me` | Get current user profile | Yes |

### Course Endpoints

| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| GET | `/courses` | Get all active courses | No | - |
| GET | `/courses/{id}` | Get course by ID | No | - |
| POST | `/courses` | Create a course | Yes | Admin |
| PUT | `/courses/{id}` | Update a course | Yes | Admin |
| PATCH | `/courses/{id}/activate` | Activate/deactivate course | Yes | Admin |

### Enrollment Endpoints

| Method | Endpoint | Description | Auth Required | Role |
|--------|----------|-------------|---------------|------|
| POST | `/enrollments` | Enroll in a course | Yes | Student |
| DELETE | `/enrollments/{course_id}` | Deregister from course | Yes | Student |
| GET | `/enrollments` | Get all enrollments | Yes | Admin |
| GET | `/enrollments/course/{id}` | Get course enrollments | Yes | Admin |
| DELETE | `/enrollments/{id}/admin` | Remove student from course | Yes | Admin |

## 🔐 Authentication

### Register a User

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123",
    "role": "student"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john@example.com&password=password123"
```

### Use Token

```bash
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 📝 Business Rules

### Enrollment Rules

- ✅ Only authenticated students can enroll
- ✅ Cannot enroll in the same course twice
- ✅ Enrollment fails if course is full
- ✅ Enrollment fails if course is inactive
- ✅ Students can deregister from courses

### Course Rules

- ✅ Course code must be unique
- ✅ Capacity must be greater than zero
- ✅ Only admins can create/update/activate courses

### User Rules

- ✅ Email must be unique
- ✅ Inactive users cannot authenticate
- ✅ Passwords are securely hashed

## 🧪 Test Coverage

The test suite includes:

- ✅ Authentication tests (registration, login, token validation)
- ✅ User management tests (profile retrieval)
- ✅ Course management tests (CRUD operations, authorization)
- ✅ Enrollment tests (business rules, capacity, duplicates)
- ✅ Authorization tests (RBAC enforcement)
- ✅ Validation tests (input validation, error handling)

## 🚢 Deployment

### Render Deployment (Recommended)

**Quick Deploy to Render:**

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/course-enrollment-platform.git
   git push -u origin main
   ```

2. **Create Web Service on Render:**
   - Go to https://dashboard.render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Build Command**: `./build.sh`
     - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Add PostgreSQL Database:**
   - Click "New +" → "PostgreSQL"
   - Copy the Internal Database URL

4. **Set Environment Variables:**
   ```
   DATABASE_URL=<your-postgres-url>
   SECRET_KEY=<generate-secure-key>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   DEBUG=False
   ```

5. **Deploy!** Render will automatically build and deploy your app.

**See [DEPLOIEMENT_RENDER.md](DEPLOIEMENT_RENDER.md) for detailed French instructions.**

### Other Platforms

**Railway, Heroku, or AWS:**

```env
DATABASE_URL=postgresql://user:pass@host:5432/dbname
SECRET_KEY=generate-a-strong-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=False
```

### Deployment Platforms

**Render, Railway, or Heroku:**
1. Create a new web service
2. Connect your repository
3. Set environment variables
4. Add PostgreSQL database
5. Deploy!

**Build Command:**
```bash
pip install -r requirements.txt && alembic upgrade head
```

**Start Command:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## 🤝 Contributing

This is a school project for AltSchool of Engineering.

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

Created as part of the AltSchool of Engineering Backend Development course.

## 📞 Support

For issues or questions, please check the API documentation at `/docs` or contact the development team.

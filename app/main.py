from fastapi import FastAPI, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routers import auth, users, courses, enrollments

# Create FastAPI application
app = FastAPI(
    title="Course Enrollment Platform API",
    description="A secure, database-backed RESTful API for managing course enrollments",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(enrollments.router)


@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Course Enrollment Platform API is running",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
def health():
    """Alternative health check endpoint"""
    return {"status": "ok"}


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled exceptions (DEBUG MODE ENABLED)"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc), "type": type(exc).__name__}
    )

from sqlalchemy import Column, Integer, String, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Course(Base):
    """Course model for managing courses"""
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Add check constraint for capacity
    __table_args__ = (
        CheckConstraint('capacity > 0', name='check_capacity_positive'),
    )
    
    # Relationships
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    
    @property
    def enrolled_count(self):
        """Get the number of students enrolled"""
        return len(self.enrollments)
    
    @property
    def available_slots(self):
        """Get the number of available slots"""
        return self.capacity - self.enrolled_count
    
    @property
    def is_full(self):
        """Check if the course is full"""
        return self.enrolled_count >= self.capacity
    
    def __repr__(self):
        return f"<Course(id={self.id}, code={self.code}, title={self.title})>"

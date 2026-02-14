import { useEffect, useState } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { Book, Users, Calendar } from 'lucide-react';

const CourseList = () => {
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(true);
    const { user } = useAuth();
    const [enrolling, setEnrolling] = useState(null);

    useEffect(() => {
        const fetchCourses = async () => {
            try {
                const response = await api.get('/courses');
                setCourses(response.data);
            } catch (error) {
                console.error('Failed to fetch courses', error);
            } finally {
                setLoading(false);
            }
        };
        fetchCourses();
    }, []);

    const handleEnroll = async (courseId) => {
        if (!user) {
            alert('Please login to enroll');
            return;
        }
        setEnrolling(courseId);
        try {
            await api.post('/enrollments', { course_id: courseId });
            alert('Enrolled successfully!');
            // Refresh courses to update capacity if needed, or just UI
        } catch (error) {
            alert(error.response?.data?.detail || 'Enrollment failed');
        } finally {
            setEnrolling(null);
        }
    };

    if (loading) return <div>Loading courses...</div>;

    return (
        <div>
            <div className="flex justify-between items-center mb-4">
                <h1 className="page-title" style={{ marginBottom: 0 }}>Available Courses</h1>
                {/* Search bar could go here */}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {courses.map((course) => (
                    <div key={course.id} className="card flex flex-col justify-between">
                        <div>
                            <div className="flex justify-between items-start mb-2">
                                <span className="badge" style={{ backgroundColor: '#e0e7ff', color: '#3730a3' }}>{course.code}</span>
                                {course.is_full ? <span className="badge badge-danger">Full</span> : <span className="badge badge-success">Available</span>}
                            </div>
                            <h3 style={{ fontSize: '1.25rem', fontWeight: '600', marginBottom: '0.5rem' }}>{course.title}</h3>
                            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '1rem', lineHeight: '1.5' }}>
                                {course.description || "No description available."}
                            </p>

                            <div className="flex items-center gap-4" style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                                <span className="flex items-center gap-1"><Users size={16} /> {course.enrolled_count} / {course.capacity}</span>
                                {/* <span className="flex items-center gap-1"><Calendar size={16} /> Spring 2024</span> */}
                            </div>
                        </div>

                        <div className="mt-4">
                            {user?.role === 'student' ? (
                                <button
                                    className="btn btn-primary"
                                    style={{ width: '100%' }}
                                    onClick={() => handleEnroll(course.id)}
                                    disabled={course.is_full || enrolling === course.id}
                                >
                                    {enrolling === course.id ? 'Enrolling...' : (course.is_full ? 'Class Full' : 'Enroll Now')}
                                </button>
                            ) : user?.role === 'admin' ? (
                                <button className="btn btn-secondary" style={{ width: '100%' }} disabled>Admin View</button>
                            ) : (
                                <button className="btn btn-secondary" style={{ width: '100%' }} disabled>Login to Enroll</button>
                            )}
                        </div>
                    </div>
                ))}
            </div>
            {courses.length === 0 && <p style={{ textAlign: 'center', color: 'var(--text-muted)', marginTop: '2rem' }}>No active courses available at the moment.</p>}
        </div>
    );
};

export default CourseList;

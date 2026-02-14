import { useEffect, useState } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';

const MyEnrollments = () => {
    const { user } = useAuth();
    const [enrollments, setEnrollments] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchEnrollments = async () => {
            try {
                const response = await api.get('/users/me');
                setEnrollments(response.data.enrollments || []);
            } catch (error) {
                console.error('Failed to fetch enrollments', error);
            } finally {
                setLoading(false);
            }
        };
        fetchEnrollments();
    }, [user]);

    const handleDrop = async (courseId) => {
        if (!confirm('Are you sure you want to drop this course?')) return;
        try {
            await api.delete(`/enrollments/${courseId}`);
            setEnrollments(enrollments.filter(e => e.course_id !== courseId));
        } catch (error) {
            alert('Failed to drop course');
        }
    };

    if (loading) return <div>Loading enrollments...</div>;

    return (
        <div>
            <h1 className="page-title">My Enrollments</h1>

            {enrollments.length === 0 ? (
                <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
                    <p style={{ color: 'var(--text-muted)', marginBottom: '1rem' }}>You haven't enrolled in any courses yet.</p>
                    <a href="/" className="btn btn-primary">Browse Courses</a>
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {enrollments.map((enrollment) => (
                        <div key={enrollment.id} className="card">
                            <div className="flex justify-between items-start">
                                <div>
                                    <span className="badge" style={{ backgroundColor: '#e0e7ff', color: '#3730a3', marginBottom: '0.5rem' }}>
                                        {enrollment.course.code}
                                    </span>
                                    <h3 style={{ fontSize: '1.25rem', fontWeight: '600' }}>{enrollment.course.title}</h3>
                                </div>
                                <button onClick={() => handleDrop(enrollment.course.id)} className="btn btn-secondary" style={{ color: 'var(--danger)', borderColor: 'var(--danger)' }}>
                                    Drop
                                </button>
                            </div>
                            <div className="mt-4" style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                                Enrolled on: {new Date(enrollment.created_at).toLocaleDateString()}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default MyEnrollments;

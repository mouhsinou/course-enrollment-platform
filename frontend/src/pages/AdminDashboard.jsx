import { useEffect, useState } from 'react';
import api from '../services/api';

const AdminDashboard = () => {
    const [courses, setCourses] = useState([]);
    const [enrollments, setEnrollments] = useState([]);
    const [stats, setStats] = useState({ totalStudents: 0, totalCourses: 0, activeEnrollments: 0 });
    const [showForm, setShowForm] = useState(false);
    const [newCourse, setNewCourse] = useState({ title: '', code: '', capacity: 30, description: '' });

    const fetchData = async () => {
        try {
            const [coursesRes, enrollmentsRes] = await Promise.all([
                api.get('/courses'),
                api.get('/enrollments')
            ]);

            setCourses(coursesRes.data);
            setEnrollments(enrollmentsRes.data);
            setStats({
                totalCourses: coursesRes.data.length,
                activeEnrollments: enrollmentsRes.data.length,
                totalStudents: 0 // Would come from /users if we fetched it
            });
        } catch (error) {
            console.error('Failed to fetch admin data', error);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const handleCreateCourse = async (e) => {
        e.preventDefault();
        try {
            await api.post('/courses', newCourse);
            setShowForm(false);
            setNewCourse({ title: '', code: '', capacity: 30, description: '' });
            fetchData(); // Refresh list
        } catch (error) {
            alert('Failed to create course: ' + (error.response?.data?.detail || error.message));
        }
    };

    const toggleStatus = async (id, currentStatus) => {
        try {
            // Send is_active as query parameter
            await api.patch(`/courses/${id}/activate?is_active=${!currentStatus}`);
            fetchData();
        } catch (error) {
            alert('Failed to update status: ' + (error.response?.data?.detail || error.message));
        }
    };

    const handleDeleteEnrollment = async (enrollmentId) => {
        if (!confirm('Êtes-vous sûr de vouloir retirer cet étudiant du cours ?')) return;
        try {
            // DELETE /enrollments/{id}/admin
            await api.delete(`/enrollments/${enrollmentId}/admin`);
            fetchData();
        } catch (error) {
            alert('Failed to remove enrollment: ' + (error.response?.data?.detail || error.message));
        }
    };

    return (
        <div>
            <div className="flex justify-between items-center mb-4">
                <h1 className="page-title" style={{ marginBottom: 0 }}>Admin Dashboard</h1>
                <button onClick={() => setShowForm(!showForm)} className="btn btn-primary">
                    {showForm ? 'Annuler' : 'Créer un Cours'}
                </button>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                <div className="card" style={{ textAlign: 'center', padding: '1.5rem' }}>
                    <h3 style={{ fontSize: '2rem', marginBottom: '0.5rem', color: 'var(--primary)' }}>{stats.totalCourses}</h3>
                    <p style={{ color: 'var(--text-muted)' }}>Total Cours</p>
                </div>
                <div className="card" style={{ textAlign: 'center', padding: '1.5rem' }}>
                    <h3 style={{ fontSize: '2rem', marginBottom: '0.5rem', color: 'var(--success)' }}>{stats.activeEnrollments}</h3>
                    <p style={{ color: 'var(--text-muted)' }}>Inscriptions Actives</p>
                </div>
            </div>

            {showForm && (
                <div className="card mb-8" style={{ backgroundColor: '#f8fafc' }}>
                    <h3>Nouveau Cours</h3>
                    <form onSubmit={handleCreateCourse} className="mt-4">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label className="label">Titre</label>
                                <input className="input" value={newCourse.title} onChange={e => setNewCourse({ ...newCourse, title: e.target.value })} required />
                            </div>
                            <div>
                                <label className="label">Code</label>
                                <input className="input" value={newCourse.code} onChange={e => setNewCourse({ ...newCourse, code: e.target.value })} required />
                            </div>
                            <div>
                                <label className="label">Capacité</label>
                                <input className="input" type="number" value={newCourse.capacity} onChange={e => setNewCourse({ ...newCourse, capacity: parseInt(e.target.value) })} required />
                            </div>
                            <div>
                                <label className="label">Description (Optionnel)</label>
                                <input className="input" value={newCourse.description} onChange={e => setNewCourse({ ...newCourse, description: e.target.value })} />
                            </div>
                        </div>
                        <button type="submit" className="btn btn-primary mt-4">Sauvegarder</button>
                    </form>
                </div>
            )}

            <div className="card mb-8">
                <h3>Gestion des Cours</h3>
                <div style={{ overflowX: 'auto' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
                        <thead>
                            <tr style={{ textAlign: 'left', borderBottom: '1px solid var(--border)' }}>
                                <th style={{ padding: '0.75rem' }}>Code</th>
                                <th style={{ padding: '0.75rem' }}>Titre</th>
                                <th style={{ padding: '0.75rem' }}>Capacité</th>
                                <th style={{ padding: '0.75rem' }}>Statut</th>
                                <th style={{ padding: '0.75rem' }}>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {courses.map(course => (
                                <tr key={course.id} style={{ borderBottom: '1px solid var(--border)' }}>
                                    <td style={{ padding: '0.75rem' }}>{course.code}</td>
                                    <td style={{ padding: '0.75rem', fontWeight: '500' }}>{course.title}</td>
                                    <td style={{ padding: '0.75rem' }}>{course.enrolled_count} / {course.capacity}</td>
                                    <td style={{ padding: '0.75rem' }}>
                                        <span className={`badge ${course.is_active ? 'badge-success' : 'badge-danger'}`}>
                                            {course.is_active ? 'Actif' : 'Inactif'}
                                        </span>
                                    </td>
                                    <td style={{ padding: '0.75rem' }}>
                                        <button onClick={() => toggleStatus(course.id, course.is_active)} className="btn btn-secondary" style={{ padding: '0.25rem 0.5rem', fontSize: '0.8rem' }}>
                                            {course.is_active ? 'Désactiver' : 'Activer'}
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>

            <div className="card">
                <h3>Gestion des Inscriptions</h3>
                <div style={{ overflowX: 'auto' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
                        <thead>
                            <tr style={{ textAlign: 'left', borderBottom: '1px solid var(--border)' }}>
                                <th style={{ padding: '0.75rem' }}>Étudiant</th>
                                <th style={{ padding: '0.75rem' }}>Cours</th>
                                <th style={{ padding: '0.75rem' }}>Date</th>
                                <th style={{ padding: '0.75rem' }}>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {enrollments.map(enrollment => (
                                <tr key={enrollment.id} style={{ borderBottom: '1px solid var(--border)' }}>
                                    <td style={{ padding: '0.75rem' }}>
                                        <div style={{ fontWeight: '500' }}>{enrollment.user?.name || 'Unknown'}</div>
                                        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{enrollment.user?.email}</div>
                                    </td>
                                    <td style={{ padding: '0.75rem' }}>
                                        <div style={{ fontWeight: '500' }}>{enrollment.course?.title || 'Unknown'}</div>
                                        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{enrollment.course?.code}</div>
                                    </td>
                                    <td style={{ padding: '0.75rem' }}>{new Date(enrollment.created_at).toLocaleDateString()}</td>
                                    <td style={{ padding: '0.75rem' }}>
                                        <button onClick={() => handleDeleteEnrollment(enrollment.id)} className="btn btn-secondary" style={{ color: 'var(--danger)', borderColor: 'var(--danger)', padding: '0.25rem 0.5rem', fontSize: '0.8rem' }}>
                                            Supprimer
                                        </button>
                                    </td>
                                </tr>
                            ))}
                            {enrollments.length === 0 && (
                                <tr><td colSpan="4" style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>Aucune inscription trouvée.</td></tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default AdminDashboard;

import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { BookOpen, LogOut, User, LayoutDashboard } from 'lucide-react';

const Navbar = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <nav style={{
            backgroundColor: 'var(--surface)',
            borderBottom: '1px solid var(--border)',
            padding: '1rem 0',
            position: 'sticky',
            top: 0,
            zIndex: 10
        }}>
            <div className="container flex justify-between items-center">
                <Link to="/" className="flex items-center gap-2" style={{ fontSize: '1.25rem', fontWeight: '700', color: 'var(--primary)' }}>
                    <BookOpen />
                    <span>CoursePlatform</span>
                </Link>

                <div className="flex items-center gap-4">
                    <Link to="/" className="btn btn-secondary" style={{ border: 'none' }}>Courses</Link>

                    {user ? (
                        <>
                            {user.role === 'student' && (
                                <Link to="/my-enrollments" className="btn btn-secondary" style={{ border: 'none' }}>My Enrollments</Link>
                            )}
                            {user.role === 'admin' && (
                                <Link to="/admin" className="btn btn-secondary" style={{ border: 'none', color: 'var(--secondary)' }}>
                                    <LayoutDashboard size={18} /> Admin
                                </Link>
                            )}

                            <div className="flex items-center gap-4" style={{ marginLeft: '1rem', paddingLeft: '1rem', borderLeft: '1px solid var(--border)' }}>
                                <span className="flex items-center gap-2" style={{ fontWeight: '500' }}>
                                    <User size={18} /> {user.name}
                                </span>
                                <button onClick={handleLogout} className="btn btn-danger" style={{ padding: '0.4rem 0.8rem', fontSize: '0.85rem' }}>
                                    <LogOut size={16} /> Logout
                                </button>
                            </div>
                        </>
                    ) : (
                        <>
                            <Link to="/login" className="btn btn-secondary">Login</Link>
                            <Link to="/register" className="btn btn-primary">Get Started</Link>
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
};

export default Navbar;

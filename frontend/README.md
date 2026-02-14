# Course Enrollment Platform - Frontend

This is the React frontend for the Course Enrollment Platform.

## 🚀 Getting Started

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The application will start at `http://localhost:5173`.
It is configured to proxy API requests to `http://localhost:8000`.

**Make sure the Backend is running on port 8000!**

## 📁 Structure

- `src/api`: Axios setup and API calls
- `src/context`: Authentication state management
- `src/pages`: Application pages (Login, Register, Dashboard, etc.)
- `src/components`: Reusable components (Navbar, ProtectedRoute)

## 🔑 Features

- **Authentication**: Login/Register with JWT
- **Student Portal**: View courses, enroll, drop courses
- **Admin Portal**: Manage courses, view enrollments
- **Responsive Design**: Works on mobile and desktop

import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import LoginPage from './pages/Auth/LoginPage';
import AssistantRoutes from './routes/AssistantRoutes';
import ClientRoutes from './routes/ClientRoutes';
import Assignment from './routes/AssignmentRoutes';
import DashboardRoutes from './routes/DashboardRoutes';
import ServiceLogRoutes from './routes/ServiceLogRoutes';
import AuditRoutes from './routes/AuditRoutes';
import './App.css'; 

function App() {
  return (
    <Router>
      <nav className="main-navbar">
        <Link to="/dashboard" className="nav-item">대시보드</Link>
        <Link to="/assignments" className="nav-item">배정 관리</Link>
        <Link to="/clients" className="nav-item">이용자 관리</Link>
        <Link to="/assistants" className="nav-item">활동지원사 관리</Link>
        <Link to="/service-logs" className="nav-item">이용내역 관리</Link>
        <Link to="/audit" className="nav-item">점검 대비</Link>
        <Link to="/login" className="nav-item logout-btn">로그아웃</Link>
      </nav>

      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/dashboard/*" element={<DashboardRoutes />} />
        <Route path="/assistants/*" element={<AssistantRoutes />} />
        <Route path="/clients/*" element={<ClientRoutes />} />
        <Route path="/assignments/*" element={<Assignment />} />
        <Route path="/service-logs/*" element={<ServiceLogRoutes />} />
        <Route path="/audit/*" element={<AuditRoutes />} />
        <Route path="/" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;
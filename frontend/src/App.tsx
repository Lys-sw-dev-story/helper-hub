import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import LoginPage from './pages/Auth/LoginPage';
import AssistantRoutes from './pages/Assistant/AssistantRoutes';
import ClientRoutes from './pages/Client/ClientRoutes';
import './App.css'; 

function App() {
  return (
    <Router>
      <nav className="main-navbar">
        <Link to="/clients" className="nav-item">이용자 관리</Link>
        <Link to="/assistants" className="nav-item">활동지원사 관리</Link>
        <Link to="/login" className="nav-item logout-btn">로그아웃</Link>
      </nav>

      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/assistants/*" element={<AssistantRoutes />} />
        <Route path="/clients/*" element={<ClientRoutes />} />
        <Route path="/" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;
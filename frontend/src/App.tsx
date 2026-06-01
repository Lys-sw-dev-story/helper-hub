import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/Auth/LoginPage';
import AssistantRoutes from './routes/AssistantRoutes';
import ClientRoutes from './routes/ClientRoutes';
import Assignment from './routes/AssignmentRoutes';
import DashboardRoutes from './routes/DashboardRoutes';
import ServiceLogRoutes from './routes/ServiceLogRoutes';
import AuditRoutes from './routes/AuditRoutes';
import Layout from './components/layout/Layout';
import './App.css'; 

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        
        <Route element={<Layout />}>
          <Route path="/dashboard/*" element={<DashboardRoutes />} />
          <Route path="/assistants/*" element={<AssistantRoutes />} />
          <Route path="/clients/*" element={<ClientRoutes />} />
          <Route path="/assignments/*" element={<Assignment />} />
          <Route path="/service-logs/*" element={<ServiceLogRoutes />} />
          <Route path="/audit/*" element={<AuditRoutes />} />
        </Route>
        
        <Route path="/" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;
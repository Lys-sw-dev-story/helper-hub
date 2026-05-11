import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import LoginPage from './pages/Auth/LoginPage';
import ClientList from './pages/Client/ClientList';
import ClientRegister from "./pages/Client/ClientRegister";
import AssistantList from './pages/Assistant/AssistantList';
import AssistantRegister from './pages/Assistant/AssistantRegister';

function App() {
  return (
    <Router>
      <nav style={{ padding: '1rem', background: '#333', color: 'white', display: 'flex', gap: '1rem' }}>
        <Link to="/clients" style={{ color: 'white', textDecoration: 'none' }}>이용자 관리</Link>
        <Link to="/assistants" style={{ color: 'white', textDecoration: 'none' }}>조력자 관리</Link>
        <Link to="/login" style={{ color: 'gray', textDecoration: 'none', marginLeft: 'auto' }}>로그아웃</Link>
      </nav>

      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/clients" element={<ClientList />} />
        <Route path="/clients/register" element={<ClientRegister />} />
        <Route path="/assistants" element={<AssistantList />} />
        <Route path="/assistants/register" element={<AssistantRegister />} />
        <Route path="/" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
}

export default App;
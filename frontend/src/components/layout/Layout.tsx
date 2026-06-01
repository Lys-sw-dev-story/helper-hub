import { Outlet, Navigate, Link } from 'react-router-dom';

const Layout = () => {
  const isAuthenticated = !!localStorage.getItem('access_token');

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('token_type');
  };

  return (
    <>
      <nav className="main-navbar">
        <Link to="/dashboard" className="nav-item">대시보드</Link>
        <Link to="/assignments" className="nav-item">배정 관리</Link>
        <Link to="/clients" className="nav-item">이용자 관리</Link>
        <Link to="/assistants" className="nav-item">활동지원사 관리</Link>
        <Link to="/service-logs" className="nav-item">이용내역 관리</Link>
        <Link to="/audit" className="nav-item">점검 대비</Link>
        <Link to="/login" className="nav-item logout-btn" onClick={handleLogout}>로그아웃</Link>
      </nav>
      <Outlet />
    </>
  );
};

export default Layout;

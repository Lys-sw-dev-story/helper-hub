import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../../api/authApi';
import './LoginPage.css'; 

const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

const handleLogin = async (e: React.FormEvent) => {
  e.preventDefault();
  setError('');
  try {
    const response = await login(email, password);
    const myOrgName = response?.organization_name;
    localStorage.setItem('organization_name', myOrgName);

    navigate('/clients'); 
  } catch (err: any) {
    console.error(err);
    setError('이메일 또는 비밀번호가 올바르지 않습니다.');
  }
};

return (
    <div className="auth-wrapper">
      <div className="auth-card">
        <div className="auth-header">
          <h2>Helper-Hub</h2>
          <p>사회복지사 시스템에 로그인하세요.</p>
        </div>

        <form onSubmit={handleLogin} className="auth-form">
          <div className="auth-group">
            <label>이메일 계정</label>
            <input 
              type="email" 
              className="auth-input"
              value={email} 
              onChange={(e) => setEmail(e.target.value)} 
              placeholder="admin@example.com"
              required 
            />
          </div>
<<<<<<< HEAD
          <div className="input-group">
            <label>비밀번호</label>
            <input 
              type="password" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)} 
              placeholder="admin1234"
              required 
            />
          </div>
          {error && <p className="error-msg">{error}</p>}
          <button type="submit" className="login-btn">로그인</button>
=======
          
          <div className="auth-group">
            <label>비밀번호</label>
            <input 
              type="password" 
              className="auth-input"
              value={password} 
              onChange={(e) => setPassword(e.target.value)} 
              placeholder="••••••••"
              required 
            />
          </div>

          {error && <div className="auth-error">⚠️ {error}</div>}
          
          <button type="submit" className="auth-btn">로그인</button>
>>>>>>> 2week
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../../api/authApi';
import './LoginPage.css';

const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('admin@example.com');
  const [password, setPassword] = useState('admin1234');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError('');

    try {
      const response = await login({ email, password });

      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('token_type', response.token_type);

      navigate('/clients');
    } catch (err) {
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
            <label htmlFor="email">이메일 계정</label>
            <input
              id="email"
              type="email"
              className="auth-input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="admin@example.com"
              required
            />
          </div>

          <div className="auth-group">
            <label htmlFor="password">비밀번호</label>
            <input
              id="password"
              type="password"
              className="auth-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="admin1234"
              required
            />
          </div>

          {error && <div className="auth-error">⚠️ {error}</div>}

          <button type="submit" className="auth-btn">
            로그인
          </button>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
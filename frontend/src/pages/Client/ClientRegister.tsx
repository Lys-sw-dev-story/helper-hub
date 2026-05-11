import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registerClient, type ClientData } from '../../api/clientApi';

const ClientRegister: React.FC = () => {
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState<ClientData>({
    client_name: '',
    client_birth_date: '',
    client_phone: '',
    client_address: '',
    client_status: '대기',
    client_memo: '',
    organization_id: 1,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // 💡 여기서 submitData를 만듭니다! 
      // 사용자가 날짜를 선택 안 하면 ""(빈 문자열)이 되는데, 
      // 이걸 null로 바꿔야 백엔드(Python date 타입)가 에러를 안 내요.
      const submitData: ClientData = {
        ...formData,
        client_birth_date: formData.client_birth_date || null,
        client_phone: formData.client_phone || null,
        client_address: formData.client_address || null,
        client_memo: formData.client_memo || null,
      };

      console.log("보내는 데이터:", submitData); // 확인용 로그
      await registerClient(submitData);
      
      alert('이용자가 성공적으로 등록되었습니다!');
      navigate('/clients');
    } catch (err) {
      console.error(err);
      alert('등록 실패! 데이터 형식을 확인해 주세요.');
    }
  };

  return (
    <div style={containerStyle}>
      <h2 style={{ marginBottom: '1.5rem', color: '#333' }}>👵 이용자 신규 등록</h2>
      <form onSubmit={handleSubmit} style={formStyle}>
        <div style={inputGroupStyle}>
          <label>성함</label>
          <input name="client_name" placeholder="이용자 이름" onChange={handleChange} required style={inputStyle} />
        </div>

        <div style={inputGroupStyle}>
          <label>생년월일</label>
          <input name="client_birth_date" type="date" onChange={handleChange} style={inputStyle} />
        </div>

        <div style={inputGroupStyle}>
          <label>연락처</label>
          <input name="client_phone" placeholder="010-0000-0000" onChange={handleChange} style={inputStyle} />
        </div>

        <div style={inputGroupStyle}>
          <label>주소</label>
          <input name="client_address" placeholder="거주지 주소" onChange={handleChange} style={inputStyle} />
        </div>

        <div style={inputGroupStyle}>
          <label>현재 상태</label>
          <select name="client_status" onChange={handleChange} style={inputStyle}>
            <option value="대기">대기</option>
            <option value="매칭중">매칭 중</option>
            <option value="이용중">이용 중</option>
            <option value="종료">종료</option>
          </select>
        </div>

        <div style={inputGroupStyle}>
          <label>메모 및 특이사항</label>
          <textarea name="client_memo" placeholder="비고" onChange={handleChange} rows={4} style={inputStyle} />
        </div>

        <button type="submit" style={submitBtnStyle}>등록하기</button>
      </form>
    </div>
  );
};

const containerStyle: React.CSSProperties = { padding: '2rem', maxWidth: '600px', margin: '2rem auto', backgroundColor: '#fff', borderRadius: '8px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)' };
const formStyle: React.CSSProperties = { display: 'flex', flexDirection: 'column', gap: '1.2rem' };
const inputGroupStyle: React.CSSProperties = { display: 'flex', flexDirection: 'column', gap: '0.5rem', textAlign: 'left' };
const inputStyle: React.CSSProperties = { padding: '0.8rem', border: '1px solid #ddd', borderRadius: '4px', fontSize: '1rem' };
const submitBtnStyle: React.CSSProperties = { padding: '1rem', backgroundColor: '#4A90E2', color: 'white', border: 'none', borderRadius: '4px', fontSize: '1.1rem', fontWeight: 'bold', cursor: 'pointer', marginTop: '1rem' };

export default ClientRegister;
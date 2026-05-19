import React from 'react';
import { Routes, Route } from 'react-router-dom';
import AssignmentList from '../pages/Assignment/AssignmentList';
import AssignmentForm from '../pages/Assignment/AssignmentForm';
import AssignmentDetail from '../pages/Assignment/AssignmentDetail'; // 상세 추가

const AssignmentRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<AssignmentList />} />
      <Route path="/new" element={<AssignmentForm />} />
      <Route path="/:id" element={<AssignmentDetail />} /> {/* 동적 라우팅 파라미터 :id */}
    </Routes>
  );
};

export default AssignmentRoutes;
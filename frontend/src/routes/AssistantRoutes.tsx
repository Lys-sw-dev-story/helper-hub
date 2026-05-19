// frontend/src/pages/Assistant/AssistantRoutes.tsx
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import AssistantList from './AssistantList';
import AssistantRegister from './AssistantRegister';
import AssistantDetail from './AssistantDetail';
import AssistantEdit from './AssistantEdit';

const AssistantRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<AssistantList />} />
      <Route path="/register" element={<AssistantRegister />} />
      <Route path="/:id" element={<AssistantDetail />} />
      <Route path="/:id/edit" element={<AssistantEdit />} />
    </Routes>
  );
};

export default AssistantRoutes;
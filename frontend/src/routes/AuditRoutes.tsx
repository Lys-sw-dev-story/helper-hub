import React from 'react';
import { Routes, Route } from 'react-router-dom';
import AuditPage from '../pages/Audit/AuditPage';

function AuditRoutes() {
  return (
    <Routes>
      <Route path="/" element={<AuditPage />} />
    </Routes>
  );
}

export default AuditRoutes;

import React from 'react';
import { Routes, Route } from 'react-router-dom';
import ServiceLogList from '../pages/ServiceLog/ServiceLogList';
import ServiceLogForm from '../pages/ServiceLog/ServiceLogForm';

function ServiceLogRoutes() {
  return (
    <Routes>
      <Route path="/" element={<ServiceLogList />} />
      <Route path="/new" element={<ServiceLogForm />} />
      <Route path="/:id/edit" element={<ServiceLogForm />} />
    </Routes>
  );
}

export default ServiceLogRoutes;

import React from 'react';
import { Routes, Route } from 'react-router-dom';
import ServiceLogList from '../pages/ServiceLog/ServiceLogList';

function ServiceLogRoutes() {
  return (
    <Routes>
      <Route path="/" element={<ServiceLogList />} />
    </Routes>
  );
}

export default ServiceLogRoutes;

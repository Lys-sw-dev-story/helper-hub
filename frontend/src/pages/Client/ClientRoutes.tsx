import React from 'react';
import { Routes, Route } from 'react-router-dom';
import ClientList from './ClientList';
import ClientRegister from './ClientRegister';
import ClientDetail from './ClientDetail';
import ClientEdit from './ClientEdit';

const ClientRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<ClientList />} />
      <Route path="/register" element={<ClientRegister />} />
      <Route path="/:id" element={<ClientDetail />} />
      <Route path="/:id/edit" element={<ClientEdit />} />
    </Routes>
  );
};

export default ClientRoutes;
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import ClientList from "../pages/Client/ClientList";
import ClientRegister from "../pages/Client/ClientRegister";
import ClientDetail from "../pages/Client/ClientDetail";
import ClientEdit from "../pages/Client/ClientEdit";

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
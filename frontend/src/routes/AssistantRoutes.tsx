import React from "react";
import { Routes, Route } from "react-router-dom";
import AssistantList from "../pages/Assistant/AssistantList";
import AssistantRegister from "../pages/Assistant/AssistantRegister";
import AssistantDetail from "../pages/Assistant/AssistantDetail";
import AssistantEdit from "../pages/Assistant/AssistantEdit";

function AssistantRoutes() {
  return (
    <Routes>
      <Route path="/" element={<AssistantList />} />
      <Route path="/register" element={<AssistantRegister />} />
      <Route path="/:assistantId" element={<AssistantDetail />} />
      <Route path="/:assistantId/edit" element={<AssistantEdit />} />
    </Routes>
  );
}

export default AssistantRoutes;
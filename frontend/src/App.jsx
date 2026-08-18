import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/layout/Sidebar';
import DashboardPage from './pages/DashboardPage';
import ComplaintsListPage from './pages/ComplaintsListPage';
import CreateComplaintPage from './pages/CreateComplaintPage';
import ComplaintDetailPage from './pages/ComplaintDetailPage';

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <Sidebar />
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/complaints" element={<ComplaintsListPage />} />
          <Route path="/complaints/new" element={<CreateComplaintPage />} />
          <Route path="/complaints/:id" element={<ComplaintDetailPage />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

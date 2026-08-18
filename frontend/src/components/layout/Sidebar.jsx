import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, FileText, PlusCircle, ShieldCheck } from 'lucide-react';

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <ShieldCheck size={26} color="#60a5fa" />
          <span>Aivoa QMS</span>
        </div>
        <span className="sidebar-tag">Pharma</span>
      </div>

      <nav className="sidebar-nav">
        <NavLink to="/dashboard" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
          <LayoutDashboard size={18} />
          <span>Dashboard</span>
        </NavLink>

        <NavLink to="/complaints" end className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
          <FileText size={18} />
          <span>Complaints</span>
        </NavLink>

        <NavLink to="/complaints/new" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
          <PlusCircle size={18} />
          <span>Create Complaint</span>
        </NavLink>
      </nav>

      <div className="sidebar-footer">
        <div style={{ fontWeight: 600, color: '#e2e8f0', marginBottom: 2 }}>Aivoa.ai QMS v1.0</div>
        <div>ICH Q9 / Q10 Compliant</div>
      </div>
    </aside>
  );
}

import React from 'react';
import { UserCheck } from 'lucide-react';

export default function Topbar({ title }) {
  return (
    <header className="topbar">
      <h1 className="page-title">{title}</h1>
      
      <div className="topbar-actions">
        <div className="system-status">
          <span className="status-dot"></span>
          <span>LangGraph AI Ready (gemma2-9b-it)</span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: '0.875rem', fontWeight: 500 }}>
          <div style={{ background: '#f1f5f9', padding: 6, borderRadius: '50%', display: 'flex' }}>
            <UserCheck size={18} color="#475569" />
          </div>
          <span>Quality Assurance Specialist</span>
        </div>
      </div>
    </header>
  );
}

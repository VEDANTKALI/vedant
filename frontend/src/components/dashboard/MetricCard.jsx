import React from 'react';

export default function MetricCard({ title, value, icon: Icon, color = '#2563eb', bg = '#eff6ff' }) {
  return (
    <div className="metric-card">
      <div>
        <div className="metric-label">{title}</div>
        <div className="metric-value">{value}</div>
      </div>
      {Icon && (
        <div className="metric-icon" style={{ backgroundColor: bg, color: color }}>
          <Icon size={24} />
        </div>
      )}
    </div>
  );
}

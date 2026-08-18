import React from 'react';

export function StatusBadge({ status }) {
  let badgeClass = 'badge-status-new';
  let label = status;

  if (status === 'UNDER_INVESTIGATION') {
    badgeClass = 'badge-status-inv';
    label = 'Under Investigation';
  } else if (status === 'ESCALATED') {
    badgeClass = 'badge-status-esc';
    label = 'Escalated';
  } else if (status === 'CLOSED') {
    badgeClass = 'badge-status-closed';
    label = 'Closed';
  } else if (status === 'NEW') {
    label = 'New';
  }

  return <span className={`badge ${badgeClass}`}>{label}</span>;
}

export function RiskBadge({ level }) {
  let badgeClass = 'badge-risk-low';

  if (level === 'Medium') {
    badgeClass = 'badge-risk-medium';
  } else if (level === 'High') {
    badgeClass = 'badge-risk-high';
  } else if (level === 'Critical') {
    badgeClass = 'badge-risk-critical';
  }

  return <span className={`badge ${badgeClass}`}>{level || 'Low'} Risk</span>;
}

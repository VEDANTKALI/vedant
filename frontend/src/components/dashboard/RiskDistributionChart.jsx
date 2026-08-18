import React from 'react';
import { ShieldAlert, AlertTriangle, ShieldCheck, Flame } from 'lucide-react';

export default function RiskDistributionChart({ riskDistribution = {} }) {
  const low = riskDistribution.Low || 0;
  const medium = riskDistribution.Medium || 0;
  const high = riskDistribution.High || 0;
  const critical = riskDistribution.Critical || 0;
  
  const total = low + medium + high + critical || 1;

  const items = [
    { label: 'Low Risk', count: low, color: '#059669', bg: '#ecfdf5', icon: ShieldCheck, pct: Math.round((low / total) * 100) },
    { label: 'Medium Risk', count: medium, color: '#d97706', bg: '#fffbeb', icon: AlertTriangle, pct: Math.round((medium / total) * 100) },
    { label: 'High Risk', count: high, color: '#e11d48', bg: '#fff1f2', icon: ShieldAlert, pct: Math.round((high / total) * 100) },
    { label: 'Critical Risk', count: critical, color: '#991b1b', bg: '#fee2e2', icon: Flame, pct: Math.round((critical / total) * 100) },
  ];

  return (
    <div className="card">
      <div className="card-header">
        <h3 className="card-title">Risk Level Distribution (ICH Q9 Matrix)</h3>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: 16 }}>
        {items.map((item, idx) => {
          const Icon = item.icon;
          return (
            <div key={idx} style={{ background: item.bg, border: `1px solid ${item.color}30`, borderRadius: 8, padding: 16 }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 8 }}>
                <span style={{ fontSize: '0.8rem', fontWeight: 600, color: item.color }}>{item.label}</span>
                <Icon size={18} color={item.color} />
              </div>
              <div style={{ fontSize: '1.5rem', fontWeight: 700, color: item.color }}>{item.count}</div>
              <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: 4 }}>{item.pct}% of total</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

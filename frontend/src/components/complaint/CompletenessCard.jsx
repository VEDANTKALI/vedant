import React from 'react';
import { AlertCircle, CheckCircle2 } from 'lucide-react';

export default function CompletenessCard({ score = 0, missingFields = [] }) {
  const isHigh = score >= 80;
  const isMedium = score >= 50 && score < 80;
  const color = isHigh ? '#059669' : isMedium ? '#d97706' : '#dc2626';
  const bg = isHigh ? '#ecfdf5' : isMedium ? '#fffbeb' : '#fef2f2';

  return (
    <div className="card" style={{ background: bg, border: `1px solid ${color}40` }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 12 }}>
        <div>
          <h4 style={{ fontSize: '0.9rem', fontWeight: 600, color: '#0f172a' }}>Complaint Completeness</h4>
          <div style={{ fontSize: '0.78rem', color: '#64748b' }}>QMS Required Fields Compliance</div>
        </div>
        <div style={{ fontSize: '1.6rem', fontWeight: 800, color: color }}>
          {score}%
        </div>
      </div>

      <div style={{ height: 8, background: '#e2e8f0', borderRadius: 4, overflow: 'hidden', marginBottom: 16 }}>
        <div style={{ width: `${score}%`, height: '100%', backgroundColor: color, transition: 'width 0.4s ease' }}></div>
      </div>

      {missingFields && missingFields.length > 0 ? (
        <div>
          <div style={{ fontSize: '0.8rem', fontWeight: 600, color: '#991b1b', marginBottom: 6, display: 'flex', alignItems: 'center', gap: 6 }}>
            <AlertCircle size={14} />
            <span>Missing Required Information ({missingFields.length})</span>
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
            {missingFields.map((f, i) => (
              <span key={i} style={{ background: '#ffffff', color: '#be123c', border: '1px solid #fecdd3', fontSize: '0.75rem', fontWeight: 500, padding: '2px 8px', borderRadius: 12 }}>
                • {f}
              </span>
            ))}
          </div>
        </div>
      ) : (
        <div style={{ fontSize: '0.825rem', color: '#047857', display: 'flex', alignItems: 'center', gap: 6, fontWeight: 500 }}>
          <CheckCircle2 size={16} />
          <span>All mandatory QMS fields are complete.</span>
        </div>
      )}
    </div>
  );
}

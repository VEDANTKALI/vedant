import React from 'react';
import { RiskBadge } from '../common/StatusBadge';
import { ShieldAlert, CheckCircle2, AlertOctagon, Info } from 'lucide-react';

export default function RiskAssessmentCard({ riskAssessment, complaint = {} }) {
  const risk = riskAssessment || {
    risk_level: complaint.risk_level || 'Low',
    severity: complaint.severity || 'Minor',
    patient_impact: complaint.patient_impact || 'None',
    investigation_required: complaint.investigation_required ?? true,
    rationale: 'Calculated using ICH Q9 Quality Risk Management framework.',
    recommended_actions: []
  };

  const actions = risk.recommended_actions || [];

  return (
    <div className="copilot-panel">
      <div className="copilot-header">
        <div className="copilot-icon">
          <ShieldAlert size={22} />
        </div>
        <div>
          <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#0f172a' }}>AI COPILOT — Risk Assessment</h3>
          <div style={{ fontSize: '0.78rem', color: '#64748b' }}>ICH Q9 Quality Risk Management Methodology</div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 20 }}>
        <div style={{ background: '#ffffff', padding: 12, borderRadius: 8, border: '1px solid #e2e8f0' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: '#64748b', textTransform: 'uppercase' }}>Risk Level</div>
          <div style={{ marginTop: 4 }}>
            <RiskBadge level={risk.risk_level} />
          </div>
        </div>

        <div style={{ background: '#ffffff', padding: 12, borderRadius: 8, border: '1px solid #e2e8f0' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: '#64748b', textTransform: 'uppercase' }}>Severity</div>
          <div style={{ fontSize: '0.95rem', fontWeight: 700, color: '#0f172a', marginTop: 4 }}>{risk.severity}</div>
        </div>

        <div style={{ background: '#ffffff', padding: 12, borderRadius: 8, border: '1px solid #e2e8f0' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: '#64748b', textTransform: 'uppercase' }}>Patient Impact</div>
          <div style={{ fontSize: '0.95rem', fontWeight: 700, color: risk.patient_impact === 'Confirmed' ? '#be123c' : risk.patient_impact === 'Potential' ? '#b45309' : '#047857', marginTop: 4 }}>
            {risk.patient_impact}
          </div>
        </div>

        <div style={{ background: '#ffffff', padding: 12, borderRadius: 8, border: '1px solid #e2e8f0' }}>
          <div style={{ fontSize: '0.75rem', fontWeight: 600, color: '#64748b', textTransform: 'uppercase' }}>Investigation</div>
          <div style={{ fontSize: '0.95rem', fontWeight: 700, color: '#0f172a', marginTop: 4 }}>
            {risk.investigation_required ? 'REQUIRED' : 'NOT REQUIRED'}
          </div>
        </div>
      </div>

      <div style={{ marginBottom: 20 }}>
        <div style={{ fontSize: '0.85rem', fontWeight: 600, color: '#0f172a', marginBottom: 6, display: 'flex', alignItems: 'center', gap: 6 }}>
          <Info size={16} color="#2563eb" />
          <span>Technical Rationale</span>
        </div>
        <div style={{ fontSize: '0.875rem', color: '#334155', background: '#ffffff', padding: 14, borderRadius: 8, border: '1px solid #e2e8f0', lineHeight: 1.6 }}>
          {risk.rationale}
        </div>
      </div>

      {actions.length > 0 && (
        <div>
          <div style={{ fontSize: '0.85rem', fontWeight: 600, color: '#0f172a', marginBottom: 10, display: 'flex', alignItems: 'center', gap: 6 }}>
            <AlertOctagon size={16} color="#d97706" />
            <span>Recommended Actions & CAPA</span>
          </div>
          <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: 8 }}>
            {actions.map((act, idx) => (
              <li key={idx} style={{ background: '#ffffff', border: '1px solid #e2e8f0', padding: '10px 12px', borderRadius: 6, fontSize: '0.85rem', color: '#1e293b', display: 'flex', alignItems: 'flex-start', gap: 8 }}>
                <CheckCircle2 size={16} color="#059669" style={{ flexShrink: 0, marginTop: 2 }} />
                <span>{act}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

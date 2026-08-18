import React from 'react';
import { Cpu, CheckCircle2, Clock, Sparkles } from 'lucide-react';

export default function AIAnalysisPanel({ stages = [], durationMs = 0, modelName = 'gemma2-9b-it' }) {
  const allStages = [
    { label: 'Reading complaint', key: 'ingest_input' },
    { label: 'Extracting fields', key: 'extract_complaint' },
    { label: 'Validating information', key: 'validate_complaint' },
    { label: 'Classifying complaint', key: 'classify_complaint' },
    { label: 'Assessing risk', key: 'assess_risk' },
    { label: 'Checking completeness', key: 'check_completeness' },
  ];

  const completedKeys = new Set(stages.map((s) => s.stage));

  return (
    <div className="card" style={{ borderLeft: '4px solid #2563eb', background: '#ffffff' }}>
      <div className="card-header" style={{ marginBottom: 12 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <Sparkles size={20} color="#2563eb" />
          <h3 className="card-title">LangGraph AI Workflow Stages</h3>
        </div>
        <span style={{ fontSize: '0.75rem', background: '#eff6ff', color: '#1d4ed8', fontWeight: 600, padding: '2px 8px', borderRadius: 12 }}>
          {modelName}
        </span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 12, marginBottom: 16 }}>
        {allStages.map((st, idx) => {
          const isDone = completedKeys.has(st.key) || stages.length > 0;
          return (
            <div key={idx} style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: '0.85rem', color: isDone ? '#047857' : '#94a3b8', fontWeight: isDone ? 500 : 400 }}>
              <div style={{ width: 22, height: 22, borderRadius: '50%', background: isDone ? '#ecfdf5' : '#f1f5f9', border: `1px solid ${isDone ? '#a7f3d0' : '#cbd5e1'}`, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                {isDone ? <CheckCircle2 size={14} color="#059669" /> : <span style={{ fontSize: '0.7rem' }}>{idx + 1}</span>}
              </div>
              <span>{st.label}</span>
            </div>
          );
        })}
      </div>

      {durationMs > 0 && (
        <div style={{ borderTop: '1px solid #f1f5f9', paddingTop: 10, display: 'flex', alignItems: 'center', gap: 6, fontSize: '0.8rem', color: '#64748b' }}>
          <Clock size={14} />
          <span>Execution completed in <strong>{durationMs} ms</strong> via Groq LangGraph State Machine</span>
        </div>
      )}
    </div>
  );
}

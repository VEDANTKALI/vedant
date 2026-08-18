import React from 'react';
import { Loader2, AlertCircle } from 'lucide-react';

export function LoadingState({ message = 'Loading QMS data...' }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '60px 0', gap: 12 }}>
      <Loader2 size={32} className="animate-spin" color="#2563eb" style={{ animation: 'spin 1s linear infinite' }} />
      <span style={{ color: '#64748b', fontSize: '0.9rem', fontWeight: 500 }}>{message}</span>
      <style>{`@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`}</style>
    </div>
  );
}

export function ErrorState({ message = 'An unexpected error occurred.' }) {
  return (
    <div style={{ background: '#fff1f2', border: '1px solid #fecdd3', color: '#be123c', padding: 16, borderRadius: 8, display: 'flex', alignItems: 'center', gap: 12 }}>
      <AlertCircle size={20} />
      <span style={{ fontSize: '0.9rem', fontWeight: 500 }}>{message}</span>
    </div>
  );
}

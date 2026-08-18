import React from 'react';
import { Link } from 'react-router-dom';
import { StatusBadge, RiskBadge } from '../common/StatusBadge';
import { Eye, ChevronRight } from 'lucide-react';

export default function ComplaintTable({ complaints = [] }) {
  if (!complaints || complaints.length === 0) {
    return (
      <div style={{ padding: '40px 0', textAlign: 'center', color: '#64748b', fontSize: '0.9rem' }}>
        No customer complaints found in database.
      </div>
    );
  }

  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>Complaint #</th>
            <th>Product / Type</th>
            <th>Batch / Lot</th>
            <th>Category</th>
            <th>Risk Level</th>
            <th>Status</th>
            <th>Completeness</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {complaints.map((item) => (
            <tr key={item.id}>
              <td>
                <Link to={`/complaints/${item.id}`} style={{ fontWeight: 600, color: '#2563eb', textDecoration: 'none' }}>
                  {item.complaint_number}
                </Link>
              </td>
              <td>
                <div style={{ fontWeight: 500 }}>{item.product_name}</div>
                <div style={{ fontSize: '0.75rem', color: '#64748b' }}>{item.product_type}</div>
              </td>
              <td>
                <span style={{ fontFamily: 'monospace', fontSize: '0.85rem', background: '#f1f5f9', padding: '2px 6px', borderRadius: 4 }}>
                  {item.batch_number || 'N/A'}
                </span>
              </td>
              <td>{item.category}</td>
              <td>
                <RiskBadge level={item.risk_level} />
              </td>
              <td>
                <StatusBadge status={item.status} />
              </td>
              <td>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <div style={{ flex: 1, height: 6, background: '#e2e8f0', borderRadius: 3, overflow: 'hidden', minWidth: 60 }}>
                    <div
                      style={{
                        width: `${item.completeness_score || 0}%`,
                        height: '100%',
                        background: item.completeness_score >= 80 ? '#10b981' : item.completeness_score >= 50 ? '#f59e0b' : '#ef4444'
                      }}
                    ></div>
                  </div>
                  <span style={{ fontSize: '0.75rem', fontWeight: 600, color: '#475569' }}>{item.completeness_score}%</span>
                </div>
              </td>
              <td>
                <Link to={`/complaints/${item.id}`} className="btn btn-secondary" style={{ padding: '4px 8px', fontSize: '0.75rem' }}>
                  <Eye size={14} />
                  <span>View</span>
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

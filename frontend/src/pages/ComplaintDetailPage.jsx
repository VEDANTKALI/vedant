import React, { useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { getComplaintById } from '../store/complaintSlice';
import Topbar from '../components/layout/Topbar';
import { StatusBadge, RiskBadge } from '../components/common/StatusBadge';
import RiskAssessmentCard from '../components/complaint/RiskAssessmentCard';
import CompletenessCard from '../components/complaint/CompletenessCard';
import { LoadingState, ErrorState } from '../components/common/LoadingState';
import { ArrowLeft, Calendar, User, Package, MapPin, Tag, ShieldCheck } from 'lucide-react';

export default function ComplaintDetailPage() {
  const { id } = useParams();
  const dispatch = useDispatch();
  const { selectedComplaint, loading, error } = useSelector((state) => state.complaints);

  useEffect(() => {
    if (id) {
      dispatch(getComplaintById(id));
    }
  }, [dispatch, id]);

  if (loading || !selectedComplaint) {
    return (
      <div className="main-content">
        <Topbar title="Complaint Details" />
        <div className="page-body">
          {error ? <ErrorState message={error} /> : <LoadingState message="Loading complaint record..." />}
        </div>
      </div>
    );
  }

  const c = selectedComplaint;
  const missingList = c.missing_fields ? (typeof c.missing_fields === 'string' ? JSON.parse(c.missing_fields) : c.missing_fields) : [];

  return (
    <div className="main-content">
      <Topbar title={`Complaint Record — ${c.complaint_number}`} />

      <div className="page-body">
        <div style={{ marginBottom: 20 }}>
          <Link to="/complaints" className="btn btn-secondary" style={{ padding: '6px 12px', fontSize: '0.825rem' }}>
            <ArrowLeft size={16} />
            <span>Back to Complaints List</span>
          </Link>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 380px', gap: 24 }}>
          {/* Main Complaint Details */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
            <div className="card">
              <div className="card-header" style={{ borderBottom: '1px solid #f1f5f9', paddingBottom: 16, marginBottom: 16 }}>
                <div>
                  <div style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: 600 }}>COMPLAINT RECORD</div>
                  <h2 style={{ fontSize: '1.4rem', fontWeight: 700, color: '#0f172a' }}>{c.product_name}</h2>
                </div>
                <div style={{ display: 'flex', gap: 8 }}>
                  <RiskBadge level={c.risk_level} />
                  <StatusBadge status={c.status} />
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 16, marginBottom: 20 }}>
                <div>
                  <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600 }}>BATCH / LOT #</div>
                  <div style={{ fontSize: '0.95rem', fontWeight: 600, fontFamily: 'monospace', color: '#1e293b' }}>
                    {c.batch_number || 'N/A'}
                  </div>
                </div>

                <div>
                  <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600 }}>CUSTOMER / REPORTER</div>
                  <div style={{ fontSize: '0.95rem', fontWeight: 600, color: '#1e293b' }}>
                    {c.customer_name || 'Anonymous / Unspecified'}
                  </div>
                </div>

                <div>
                  <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600 }}>MARKET</div>
                  <div style={{ fontSize: '0.95rem', fontWeight: 600, color: '#1e293b' }}>
                    {c.market || 'Global / Unspecified'}
                  </div>
                </div>

                <div>
                  <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600 }}>RECEIVED DATE</div>
                  <div style={{ fontSize: '0.95rem', fontWeight: 600, color: '#1e293b' }}>
                    {new Date(c.received_date).toLocaleDateString()}
                  </div>
                </div>
              </div>

              <div style={{ marginBottom: 20 }}>
                <div style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: 600, marginBottom: 4 }}>CATEGORY</div>
                <div style={{ fontSize: '0.95rem', fontWeight: 600, color: '#0f172a' }}>{c.category}</div>
              </div>

              <div>
                <div style={{ fontSize: '0.8rem', color: '#64748b', fontWeight: 600, marginBottom: 6 }}>COMPLAINT DESCRIPTION</div>
                <div style={{ background: '#f8fafc', border: '1px solid #e2e8f0', padding: 16, borderRadius: 8, fontSize: '0.9rem', color: '#334155', lineHeight: 1.6 }}>
                  {c.description}
                </div>
              </div>
            </div>
          </div>

          {/* AI Copilot & Completeness Panel */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
            <CompletenessCard
              score={c.completeness_score}
              missingFields={missingList}
            />

            <RiskAssessmentCard
              riskAssessment={c.risk_assessment}
              complaint={c}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

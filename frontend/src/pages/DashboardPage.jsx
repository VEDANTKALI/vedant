import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { getDashboardSummary } from '../store/dashboardSlice';
import Topbar from '../components/layout/Topbar';
import MetricCard from '../components/dashboard/MetricCard';
import RiskDistributionChart from '../components/dashboard/RiskDistributionChart';
import ComplaintTable from '../components/complaint/ComplaintTable';
import { LoadingState, ErrorState } from '../components/common/LoadingState';
import { FileText, Clock, ShieldAlert, CheckCircle2, Award } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function DashboardPage() {
  const dispatch = useDispatch();
  const { summary, loading, error } = useSelector((state) => state.dashboard);

  useEffect(() => {
    dispatch(getDashboardSummary());
  }, [dispatch]);

  if (loading && !summary) {
    return (
      <div className="main-content">
        <Topbar title="QMS Executive Dashboard" />
        <div className="page-body">
          <LoadingState message="Loading QMS metrics & live complaint status..." />
        </div>
      </div>
    );
  }

  if (error && !summary) {
    return (
      <div className="main-content">
        <Topbar title="QMS Executive Dashboard" />
        <div className="page-body">
          <ErrorState message={error} />
        </div>
      </div>
    );
  }

  const stats = summary || {
    total_complaints: 0,
    open_complaints: 0,
    high_risk_complaints: 0,
    under_investigation: 0,
    avg_completeness_score: 0.0,
    risk_distribution: {},
    recent_complaints: []
  };

  return (
    <div className="main-content">
      <Topbar title="QMS Executive Dashboard" />
      
      <div className="page-body">
        {/* KPI Metrics */}
        <div className="grid-metrics">
          <MetricCard
            title="Total Complaints"
            value={stats.total_complaints}
            icon={FileText}
            color="#2563eb"
            bg="#eff6ff"
          />
          <MetricCard
            title="Open Complaints"
            value={stats.open_complaints}
            icon={Clock}
            color="#d97706"
            bg="#fffbeb"
          />
          <MetricCard
            title="High / Critical Risk"
            value={stats.high_risk_complaints}
            icon={ShieldAlert}
            color="#dc2626"
            bg="#fef2f2"
          />
          <MetricCard
            title="Under Investigation"
            value={stats.under_investigation}
            icon={CheckCircle2}
            color="#059669"
            bg="#ecfdf5"
          />
          <MetricCard
            title="Avg Completeness Score"
            value={`${stats.avg_completeness_score}%`}
            icon={Award}
            color="#7c3aed"
            bg="#f5f3ff"
          />
        </div>

        {/* Risk Level Distribution */}
        <div style={{ marginBottom: 28 }}>
          <RiskDistributionChart riskDistribution={stats.risk_distribution} />
        </div>

        {/* Recent Complaints */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Recent Customer Complaints</h3>
            <Link to="/complaints" className="btn btn-secondary" style={{ fontSize: '0.8rem' }}>
              View All Complaints
            </Link>
          </div>

          <ComplaintTable complaints={stats.recent_complaints} />
        </div>
      </div>
    </div>
  );
}

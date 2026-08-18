import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { getComplaints } from '../store/complaintSlice';
import Topbar from '../components/layout/Topbar';
import ComplaintTable from '../components/complaint/ComplaintTable';
import { LoadingState, ErrorState } from '../components/common/LoadingState';
import { PlusCircle, Search, Filter } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function ComplaintsListPage() {
  const dispatch = useDispatch();
  const { items, loading, error } = useSelector((state) => state.complaints);

  const [search, setSearch] = useState('');
  const [riskFilter, setRiskFilter] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');

  useEffect(() => {
    dispatch(getComplaints({ search, risk_level: riskFilter, category: categoryFilter }));
  }, [dispatch, search, riskFilter, categoryFilter]);

  return (
    <div className="main-content">
      <Topbar title="Customer Complaints Register" />

      <div className="page-body">
        {/* Actions Bar */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 24, gap: 16, flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, flex: 1, minWidth: 280 }}>
            <div style={{ position: 'relative', flex: 1 }}>
              <Search size={18} color="#94a3b8" style={{ position: 'absolute', left: 12, top: 12 }} />
              <input
                type="text"
                placeholder="Search complaint #, product, batch, customer..."
                className="form-input"
                style={{ paddingLeft: 38 }}
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>

            <select
              className="form-select"
              style={{ width: 160 }}
              value={riskFilter}
              onChange={(e) => setRiskFilter(e.target.value)}
            >
              <option value="">All Risk Levels</option>
              <option value="Low">Low Risk</option>
              <option value="Medium">Medium Risk</option>
              <option value="High">High Risk</option>
              <option value="Critical">Critical Risk</option>
            </select>

            <select
              className="form-select"
              style={{ width: 180 }}
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
            >
              <option value="">All Categories</option>
              <option value="Product Quality">Product Quality</option>
              <option value="Packaging">Packaging</option>
              <option value="Labeling">Labeling</option>
              <option value="Wrong Strength">Wrong Strength</option>
              <option value="Adverse Event / Patient Safety">Adverse Event</option>
            </select>
          </div>

          <Link to="/complaints/new" className="btn btn-primary">
            <PlusCircle size={18} />
            <span>Create Complaint</span>
          </Link>
        </div>

        {/* Content Table */}
        {loading ? (
          <LoadingState message="Loading complaints database..." />
        ) : error ? (
          <ErrorState message={error} />
        ) : (
          <div className="card" style={{ padding: 0 }}>
            <ComplaintTable complaints={items} />
          </div>
        )}
      </div>
    </div>
  );
}

import React, { useState, useEffect } from 'react';
import { Save, RefreshCw } from 'lucide-react';

export default function ComplaintForm({ initialValues = {}, onSubmit, isSubmitting = false }) {
  const [formData, setFormData] = useState({
    customer_name: '',
    received_date: new Date().toISOString().slice(0, 16),
    product_name: '',
    product_type: 'FDF',
    batch_number: '',
    market: '',
    category: 'Product Quality',
    description: '',
    defect: '',
    quantity_affected: '',
    patient_impact: 'None',
    medical_safety_concern: false,
    severity: 'Minor',
    risk_level: 'Low',
    investigation_required: true,
    status: 'NEW',
    recommended_actions: []
  });

  useEffect(() => {
    if (initialValues) {
      setFormData((prev) => ({
        ...prev,
        ...initialValues,
        quantity_affected: initialValues.quantity_affected ?? '',
        received_date: initialValues.received_date ? new Date(initialValues.received_date).toISOString().slice(0, 16) : prev.received_date
      }));
    }
  }, [initialValues]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const payload = {
      ...formData,
      quantity_affected: formData.quantity_affected ? parseInt(formData.quantity_affected, 10) : null
    };
    if (onSubmit) {
      onSubmit(payload);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      {/* Section 1: Complaint Information */}
      <div className="card">
        <h3 className="card-title" style={{ marginBottom: 16 }}>1. Complaint Information</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 16 }}>
          <div className="form-group">
            <label className="form-label">Customer / Reporter Name</label>
            <input
              type="text"
              name="customer_name"
              className="form-input"
              value={formData.customer_name || ''}
              onChange={handleChange}
              placeholder="e.g. St. Jude Hospital / Dr. Smith"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Received Date</label>
            <input
              type="datetime-local"
              name="received_date"
              className="form-input"
              value={formData.received_date}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Product Name *</label>
            <input
              type="text"
              name="product_name"
              className="form-input"
              required
              value={formData.product_name || ''}
              onChange={handleChange}
              placeholder="e.g. Amoxicillin 250mg Capsules"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Product Type</label>
            <select name="product_type" className="form-select" value={formData.product_type} onChange={handleChange}>
              <option value="FDF">FDF (Finished Dosage Form)</option>
              <option value="API">API (Active Pharmaceutical Ingredient)</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Batch / Lot Number</label>
            <input
              type="text"
              name="batch_number"
              className="form-input"
              value={formData.batch_number || ''}
              onChange={handleChange}
              placeholder="e.g. AMX-2026-402"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Market Destination</label>
            <input
              type="text"
              name="market"
              className="form-input"
              value={formData.market || ''}
              onChange={handleChange}
              placeholder="e.g. US, EU, Germany"
            />
          </div>
        </div>
      </div>

      {/* Section 2: Complaint Details */}
      <div className="card">
        <h3 className="card-title" style={{ marginBottom: 16 }}>2. Complaint Details</h3>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginBottom: 16 }}>
          <div className="form-group">
            <label className="form-label">Category *</label>
            <select name="category" className="form-select" value={formData.category} onChange={handleChange}>
              <option value="Product Quality">Product Quality</option>
              <option value="Packaging">Packaging</option>
              <option value="Labeling">Labeling</option>
              <option value="Stability">Stability</option>
              <option value="Contamination">Contamination</option>
              <option value="Foreign Matter">Foreign Matter</option>
              <option value="Wrong Product">Wrong Product</option>
              <option value="Wrong Strength">Wrong Strength</option>
              <option value="Shipping / Distribution">Shipping / Distribution</option>
              <option value="Adverse Event / Patient Safety">Adverse Event / Patient Safety</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Defect Type</label>
            <input
              type="text"
              name="defect"
              className="form-input"
              value={formData.defect || ''}
              onChange={handleChange}
              placeholder="e.g. Discolored Tablet, Blister Pin-hole Leak"
            />
          </div>
        </div>

        <div className="form-group">
          <label className="form-label">Complaint Narrative / Description *</label>
          <textarea
            name="description"
            rows={4}
            className="form-textarea"
            required
            value={formData.description || ''}
            onChange={handleChange}
            placeholder="Detailed description of customer complaint..."
          />
        </div>

        <div className="form-group" style={{ maxWidth: 220 }}>
          <label className="form-label">Quantity Affected</label>
          <input
            type="number"
            name="quantity_affected"
            className="form-input"
            value={formData.quantity_affected}
            onChange={handleChange}
            placeholder="e.g. 5"
          />
        </div>
      </div>

      {/* Section 3: Risk & Safety Assessment */}
      <div className="card">
        <h3 className="card-title" style={{ marginBottom: 16 }}>3. Quality Risk & Patient Safety</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 16 }}>
          <div className="form-group">
            <label className="form-label">Patient Impact</label>
            <select name="patient_impact" className="form-select" value={formData.patient_impact} onChange={handleChange}>
              <option value="None">None</option>
              <option value="Potential">Potential</option>
              <option value="Confirmed">Confirmed</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Severity Level</label>
            <select name="severity" className="form-select" value={formData.severity} onChange={handleChange}>
              <option value="Minor">Minor</option>
              <option value="Major">Major</option>
              <option value="Critical">Critical</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Overall Risk Level</label>
            <select name="risk_level" className="form-select" value={formData.risk_level} onChange={handleChange}>
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
              <option value="Critical">Critical</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Workflow Status</label>
            <select name="status" className="form-select" value={formData.status} onChange={handleChange}>
              <option value="NEW">New</option>
              <option value="UNDER_INVESTIGATION">Under Investigation</option>
              <option value="ESCALATED">Escalated</option>
              <option value="CLOSED">Closed</option>
            </select>
          </div>
        </div>

        <div style={{ marginTop: 12, display: 'flex', alignItems: 'center', gap: 24 }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: 8, cursor: 'pointer', fontSize: '0.9rem', fontWeight: 500 }}>
            <input
              type="checkbox"
              name="medical_safety_concern"
              checked={formData.medical_safety_concern}
              onChange={handleChange}
            />
            <span>Medical Safety Concern Present</span>
          </label>

          <label style={{ display: 'flex', alignItems: 'center', gap: 8, cursor: 'pointer', fontSize: '0.9rem', fontWeight: 500 }}>
            <input
              type="checkbox"
              name="investigation_required"
              checked={formData.investigation_required}
              onChange={handleChange}
            />
            <span>Investigation Required (QMS Ticket)</span>
          </label>
        </div>
      </div>

      <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 12 }}>
        <button type="submit" className="btn btn-primary" disabled={isSubmitting} style={{ padding: '12px 24px', fontSize: '0.95rem' }}>
          {isSubmitting ? <RefreshCw size={18} className="animate-spin" /> : <Save size={18} />}
          <span>{isSubmitting ? 'Saving Complaint...' : 'Save Customer Complaint'}</span>
        </button>
      </div>
    </form>
  );
}

const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api';

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error('Failed to fetch backend health');
  return res.json();
}

export async function fetchDashboardSummary() {
  const res = await fetch(`${API_BASE}/dashboard/summary`);
  if (!res.ok) throw new Error('Failed to fetch dashboard summary');
  return res.json();
}

export async function fetchComplaints(params = {}) {
  const baseUrl = API_BASE.startsWith('http') ? API_BASE : `${window.location.origin}${API_BASE}`;
  const url = new URL(`${baseUrl}/complaints`);
  if (params.category) url.searchParams.append('category', params.category);
  if (params.risk_level) url.searchParams.append('risk_level', params.risk_level);
  if (params.search) url.searchParams.append('search', params.search);

  const res = await fetch(url.toString());
  if (!res.ok) throw new Error('Failed to fetch complaints list');
  return res.json();
}

export async function fetchComplaintById(id) {
  const res = await fetch(`${API_BASE}/complaints/${id}`);
  if (!res.ok) throw new Error(`Failed to fetch complaint ID ${id}`);
  return res.json();
}

export async function analyzeComplaintText(text, sourceType = 'text') {
  const res = await fetch(`${API_BASE}/complaints/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, source_type: sourceType })
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'AI analysis request failed');
  }
  return res.json();
}

export async function uploadComplaintPDF(file) {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${API_BASE}/complaints/upload-pdf`, {
    method: 'POST',
    body: formData
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'PDF upload failed');
  }
  return res.json();
}

export async function saveComplaint(complaintData) {
  const res = await fetch(`${API_BASE}/complaints`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(complaintData)
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to save complaint');
  }
  return res.json();
}

export async function updateComplaint(id, updateData) {
  const res = await fetch(`${API_BASE}/complaints/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(updateData)
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to update complaint ${id}`);
  }
  return res.json();
}

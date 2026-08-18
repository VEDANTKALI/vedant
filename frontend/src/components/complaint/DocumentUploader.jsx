import React, { useState } from 'react';
import { UploadCloud, FileText, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react';
import { uploadComplaintPDF } from '../../services/api';

export default function DocumentUploader({ onTextExtracted }) {
  const [uploading, setUploading] = useState(false);
  const [fileInfo, setFileInfo] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setError('Please upload a valid PDF document.');
      return;
    }

    setUploading(true);
    setError(null);

    try {
      const data = await uploadComplaintPDF(file);
      setFileInfo({
        name: data.filename,
        charCount: data.char_count
      });
      if (onTextExtracted) {
        onTextExtracted(data.extracted_text);
      }
    } catch (err) {
      setError(err.message || 'Failed to extract text from PDF.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div style={{ border: '2px dashed #cbd5e1', borderRadius: 8, padding: 24, textAlign: 'center', backgroundColor: '#f8fafc', transition: 'border-color 0.15s ease' }}>
      <input
        type="file"
        id="pdf-upload-input"
        accept="application/pdf"
        onChange={handleFileChange}
        style={{ display: 'none' }}
      />
      <label htmlFor="pdf-upload-input" style={{ cursor: 'pointer', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8 }}>
        <div style={{ background: '#eff6ff', color: '#2563eb', padding: 12, borderRadius: '50%' }}>
          {uploading ? <Loader2 size={24} className="animate-spin" /> : <UploadCloud size={24} />}
        </div>
        <div style={{ fontWeight: 600, fontSize: '0.95rem', color: '#0f172a' }}>
          {uploading ? 'Extracting text from PDF...' : 'Click or Drag PDF Complaint Document'}
        </div>
        <div style={{ fontSize: '0.8rem', color: '#64748b' }}>
          Supports pharmaceutical complaint letters, hospital reports, customer emails (PDF max 10MB)
        </div>
      </label>

      {fileInfo && (
        <div style={{ marginTop: 16, background: '#ecfdf5', border: '1px solid #a7f3d0', color: '#047857', padding: '10px 14px', borderRadius: 6, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8, fontSize: '0.85rem' }}>
          <CheckCircle2 size={16} />
          <span>Extracted <strong>{fileInfo.charCount}</strong> characters from <strong>{fileInfo.name}</strong></span>
        </div>
      )}

      {error && (
        <div style={{ marginTop: 16, background: '#fff1f2', border: '1px solid #fecdd3', color: '#be123c', padding: '10px 14px', borderRadius: 6, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8, fontSize: '0.85rem' }}>
          <AlertCircle size={16} />
          <span>{error}</span>
        </div>
      )}
    </div>
  );
}

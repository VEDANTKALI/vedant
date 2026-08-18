import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { analyzeComplaint, createNewComplaint, clearAIAnalysis } from '../store/complaintSlice';
import Topbar from '../components/layout/Topbar';
import DocumentUploader from '../components/complaint/DocumentUploader';
import AIAnalysisPanel from '../components/complaint/AIAnalysisPanel';
import RiskAssessmentCard from '../components/complaint/RiskAssessmentCard';
import CompletenessCard from '../components/complaint/CompletenessCard';
import ComplaintForm from '../components/complaint/ComplaintForm';
import { ErrorState } from '../components/common/LoadingState';
import { Sparkles, FileText, UploadCloud, ArrowRight } from 'lucide-react';

export default function CreateComplaintPage() {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const { aiAnalyzing, aiAnalysisResult, saving, error } = useSelector((state) => state.complaints);

  const [inputTab, setInputTab] = useState('text'); // 'text' or 'pdf'
  const [complaintText, setComplaintText] = useState('');

  const handleAnalyze = () => {
    if (!complaintText || !complaintText.trim()) return;
    dispatch(analyzeComplaint({ text: complaintText, sourceType: inputTab }));
  };

  const handleSave = async (formData) => {
    const aiComp = aiAnalysisResult?.complaint || {};
    
    const payload = {
      ...formData,
      completeness_score: aiAnalysisResult?.completeness_score || 0.0,
      missing_fields: aiAnalysisResult?.missing_fields || [],
      risk_assessment: {
        severity: formData.severity || aiComp.severity || 'Minor',
        probability: 'Possible',
        detectability: 'Medium',
        risk_level: formData.risk_level || aiComp.risk_level || 'Low',
        rationale: aiComp.rationale || 'Risk evaluated based on QMS rules.',
        recommended_actions: aiComp.recommended_actions || []
      }
    };

    const res = await dispatch(createNewComplaint(payload));
    if (createNewComplaint.fulfilled.match(res)) {
      dispatch(clearAIAnalysis());
      navigate('/complaints');
    }
  };

  const extractedData = aiAnalysisResult?.complaint || null;

  return (
    <div className="main-content">
      <Topbar title="Create New Customer Complaint" />

      <div className="page-body">
        {error && (
          <div style={{ marginBottom: 20 }}>
            <ErrorState message={error} />
          </div>
        )}

        {/* Ingestion & AI Trigger Area */}
        <div className="card" style={{ marginBottom: 28 }}>
          <div className="card-header">
            <h3 className="card-title">1. Customer Complaint Document Ingestion</h3>
            <div style={{ display: 'flex', gap: 8 }}>
              <button
                className={`btn ${inputTab === 'text' ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => setInputTab('text')}
                style={{ padding: '6px 14px', fontSize: '0.8rem' }}
              >
                <FileText size={16} />
                <span>Text / Email</span>
              </button>
              <button
                className={`btn ${inputTab === 'pdf' ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => setInputTab('pdf')}
                style={{ padding: '6px 14px', fontSize: '0.8rem' }}
              >
                <UploadCloud size={16} />
                <span>PDF Document</span>
              </button>
            </div>
          </div>

          {inputTab === 'text' ? (
            <div className="form-group" style={{ marginBottom: 16 }}>
              <textarea
                rows={5}
                className="form-textarea"
                placeholder="Paste customer complaint, hospital safety alert, or customer email text here..."
                value={complaintText}
                onChange={(e) => setComplaintText(e.target.value)}
              />
            </div>
          ) : (
            <div style={{ marginBottom: 16 }}>
              <DocumentUploader
                onTextExtracted={(text) => {
                  setComplaintText(text);
                  setInputTab('text');
                }}
              />
            </div>
          )}

          <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
            <button
              className="btn btn-primary"
              onClick={handleAnalyze}
              disabled={aiAnalyzing || !complaintText.trim()}
              style={{ padding: '10px 20px', fontSize: '0.9rem' }}
            >
              <Sparkles size={18} />
              <span>{aiAnalyzing ? 'Running LangGraph Workflow...' : 'Analyze Complaint with AI'}</span>
            </button>
          </div>
        </div>

        {/* AI Workflow Stages Panel */}
        {(aiAnalyzing || aiAnalysisResult) && (
          <div style={{ marginBottom: 28 }}>
            <AIAnalysisPanel
              stages={aiAnalysisResult?.processing_stages || []}
              durationMs={aiAnalysisResult?.processing_time_ms || 0}
              modelName={aiAnalysisResult?.model_name || 'gemma2-9b-it'}
            />
          </div>
        )}

        {/* Form and AI Copilot Layout */}
        <div style={{ display: 'grid', gridTemplateColumns: extractedData ? '1fr 380px' : '1fr', gap: 24 }}>
          <div>
            <ComplaintForm
              initialValues={extractedData || { description: complaintText }}
              onSubmit={handleSave}
              isSubmitting={saving}
            />
          </div>

          {extractedData && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
              <CompletenessCard
                score={aiAnalysisResult.completeness_score}
                missingFields={aiAnalysisResult.missing_fields}
              />

              <RiskAssessmentCard
                riskAssessment={{
                  risk_level: extractedData.risk_level,
                  severity: extractedData.severity,
                  patient_impact: extractedData.patient_impact,
                  investigation_required: extractedData.investigation_required,
                  rationale: extractedData.description ? `Extracted automatically from complaint text: ${extractedData.description.slice(0, 150)}...` : 'Evaluated via QMS workflow.',
                  recommended_actions: extractedData.recommended_actions
                }}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

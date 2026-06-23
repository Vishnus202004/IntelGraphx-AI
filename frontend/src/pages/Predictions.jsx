import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { TrendingUp, BrainCircuit, CheckCircle, XCircle } from 'lucide-react';



const Predictions = () => {
  const [predictions, setPredictions] = useState([]);

  useEffect(() => {
    const fetchPredictions = async () => {
      try {
        const res = await axios.get('http://localhost:8000/api/v1/predictions');
        setPredictions(res.data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchPredictions();
  }, []);

  const confidencePct = (c) => Math.round(c * 100);

  const confidenceColor = (c) => {
    if (c >= 0.75) return '#16a34a';
    if (c >= 0.50) return '#ca8a04';
    return '#dc2626';
  };

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '24px' }}>
        <TrendingUp size={36} color="#a78bfa" />
        <div>
          <h1>Strategic Forecasts</h1>
          <p>AI-generated predictions of your competitors' next moves based on historical patterns and recent signals.</p>
        </div>
      </div>

      <div className="grid-2">
        {predictions.map(pred => (
          <div key={pred.id} className="glass-panel" style={{ position: 'relative', overflow: 'hidden' }}>
            {/* Severity stripe */}
            <div style={{
              position: 'absolute', top: 0, left: 0, width: '4px', height: '100%',
              background: confidenceColor(pred.confidence)
            }} />

            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <BrainCircuit size={20} color="#a78bfa" />
                <h3 style={{ margin: 0, color: '#0f172a', fontSize: '15px' }}>
                  Competitor #{pred.competitor_id}
                </h3>
              </div>
              <div style={{
                background: `rgba(${pred.confidence >= 0.75 ? '22,163,74' : pred.confidence >= 0.5 ? '202,138,4' : '220,38,38'}, 0.1)`,
                padding: '4px 12px', borderRadius: '20px',
                border: `1px solid rgba(${pred.confidence >= 0.75 ? '22,163,74' : pred.confidence >= 0.5 ? '202,138,4' : '220,38,38'}, 0.25)`,
                color: confidenceColor(pred.confidence),
                fontWeight: 'bold', fontSize: '13px'
              }}>
                {confidencePct(pred.confidence)}% Confidence
              </div>
            </div>

            {/* Title */}
            <p style={{ fontWeight: '600', color: '#0f172a', marginBottom: '8px' }}>{pred.title}</p>

            {/* Content / reasoning */}
            <p style={{ color: '#64748b', fontSize: '14px', lineHeight: '1.6', marginBottom: '16px' }}>
              {pred.content}
            </p>

            {/* Verified / Missed badge */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '12px', color: '#64748b' }}>
                {new Date(pred.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
              </span>
              <details style={{ cursor: 'pointer', fontSize: '13px', color: '#3b82f6', fontWeight: 'bold' }}>
                <summary style={{ outline: 'none' }}>View Agent Reasoning</summary>
                <div style={{ marginTop: '12px', padding: '12px', background: 'rgba(0,0,0,0.02)', borderRadius: '8px', color: '#475569', fontSize: '12px', fontWeight: 'normal', borderLeft: '2px solid #cbd5e1' }}>
                  <p style={{ margin: '0 0 4px 0' }}><strong>1. Signal Detection:</strong> Identified recent strategic shifts from scraped data.</p>
                  <p style={{ margin: '0 0 4px 0' }}><strong>2. Pattern Match:</strong> Compared with historical alerts for this competitor.</p>
                  <p style={{ margin: 0 }}><strong>3. Forecast Generation:</strong> Groq LLM synthesized signals into this {confidencePct(pred.confidence)}% confidence prediction.</p>
                </div>
              </details>
              {pred.is_correct === true && (
                <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: '#16a34a', fontSize: '13px', fontWeight: 'bold' }}>
                  <CheckCircle size={14} /> Verified
                </span>
              )}
              {pred.is_correct === false && (
                <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: '#dc2626', fontSize: '13px', fontWeight: 'bold' }}>
                  <XCircle size={14} /> Missed
                </span>
              )}
              {pred.is_correct === null && (
                <span style={{ color: '#64748b', fontSize: '13px' }}>Pending Validation</span>
              )}
            </div>
          </div>
        ))}

        {predictions.length === 0 && (
          <div className="glass-panel" style={{ gridColumn: '1 / span 2', textAlign: 'center', padding: '64px' }}>
            <TrendingUp size={48} color="#475569" style={{ marginBottom: '16px' }} />
            <h3>No Forecasts Yet</h3>
            <p>Add competitors and run the pipeline — forecasts will appear here once the Groq agents have enough data to analyse.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Predictions;

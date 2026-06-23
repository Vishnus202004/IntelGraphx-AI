import React, { useState } from 'react';
import { FileText, Download, Calendar, Loader } from 'lucide-react';

const API_BASE = 'http://localhost:8000/api/v1';

const Reports = () => {
  const [downloading, setDownloading] = useState(false);

  const handleDownload = async () => {
    setDownloading(true);
    try {

      const response = await fetch(`${API_BASE}/reports/download`);
      if (!response.ok) throw new Error('Failed to generate report');

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'IntelGraphX_Weekly_Battle_Card.pdf';
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('PDF download error:', err);
      alert('Could not generate PDF. Make sure the backend is running.');
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '24px' }}>
        <FileText size={36} color="#3b82f6" />
        <div>
          <h1>Intelligence Reports</h1>
          <p>Download live PDF battle cards and executive summaries generated from your AI pipeline data.</p>
        </div>
      </div>

      <div className="grid-2">

        <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <h2>Generated Reports</h2>


          <div style={{
            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
            padding: '20px', background: 'rgba(59,130,246,0.08)',
            borderRadius: '10px', border: '1px solid rgba(59,130,246,0.2)'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
              <Calendar size={24} color="#3b82f6" />
              <div>
                <h4 style={{ margin: '0 0 4px 0' }}>Weekly Battle Card</h4>
                <div style={{ fontSize: '12px', color: '#64748b' }}>
                  Generated from live DB data · Includes all alerts &amp; forecasts
                </div>
              </div>
            </div>
            <button
              onClick={handleDownload}
              disabled={downloading}
              style={{
                display: 'flex', alignItems: 'center', gap: '8px',
                padding: '10px 20px', borderRadius: '8px',
                border: 'none',
                background: downloading ? '#e2e8f0' : 'linear-gradient(135deg,#3b82f6,#2563eb)',
                color: downloading ? '#64748b' : 'white', fontWeight: '600',
                cursor: downloading ? 'not-allowed' : 'pointer',
                transition: 'all 0.2s', whiteSpace: 'nowrap'
              }}>
              {downloading
                ? <><Loader size={16} style={{ animation: 'spin 1s linear infinite' }} /> Generating…</>
                : <><Download size={16} /> Download PDF</>}
            </button>
          </div>

          <p style={{ fontSize: '13px', color: '#64748b', margin: 0 }}>
            The PDF is generated on-demand from the latest intelligence in your database — every download reflects the most current data.
          </p>
        </div>


        <div className="glass-panel">
          <h2>Competitor Timeline</h2>
          <p>Major strategic shifts detected by your agents.</p>

          <div style={{
            marginTop: '24px',
            borderLeft: '2px solid rgba(59,130,246,0.3)',
            marginLeft: '8px',
            paddingLeft: '24px',
            display: 'flex', flexDirection: 'column', gap: '28px'
          }}>
            {[
              { dot: '#3b82f6', ago: 'Today', text: 'Pipeline started for all tracked competitors' },
              { dot: '#a78bfa', ago: '6 hrs', text: 'APScheduler will auto-trigger intelligence cycle' },
              { dot: '#22c55e', ago: 'Next Monday', text: 'First weekly email digest scheduled for delivery' },
            ].map((item, i) => (
              <div key={i} style={{ position: 'relative' }}>
                <div style={{
                  position: 'absolute', left: '-31px', top: '3px',
                  width: '12px', height: '12px', borderRadius: '50%',
                  background: item.dot, boxShadow: `0 0 8px ${item.dot}88`
                }} />
                <div style={{ fontSize: '12px', color: '#64748b', marginBottom: '4px' }}>{item.ago}</div>
                <strong style={{ color: '#0f172a' }}>{item.text}</strong>
              </div>
            ))}
          </div>
        </div>
      </div>

      <style>{`
        @keyframes spin { to { transform: rotate(360deg); } }
      `}</style>
    </div>
  );
};

export default Reports;

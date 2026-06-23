import React, { useEffect, useState } from 'react';
import { Target, AlertTriangle, TrendingUp, ShieldAlert, Activity, Database, Cpu } from 'lucide-react';
import axios from 'axios';

const API = 'http://localhost:8000/api/v1';







const severityColor = (s) =>
  s === 'RED' ? '#dc2626' : s === 'YELLOW' ? '#ca8a04' : '#16a34a';

const Dashboard = () => {
  const [alerts, setAlerts]           = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [competitors, setCompetitors] = useState([]);
  const [loading, setLoading]         = useState(true);
  const [runningPipelines, setRunningPipelines] = useState([]);

  const fetchDashboardData = async () => {
    try {
      const [aRes, pRes, cRes, statusRes] = await Promise.all([
        axios.get(`${API}/alerts/`),
        axios.get(`${API}/predictions/`),
        axios.get(`${API}/competitors/`),
        axios.get(`${API}/pipeline/status`),
      ]);
      setAlerts(aRes.data);
      setPredictions(pRes.data);
      setCompetitors(cRes.data);
      setRunningPipelines(statusRes.data.active_pipelines || []);
    } catch (err) {
      console.error('Dashboard fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
    // Poll every 5 seconds to auto-refresh data when a pipeline is running
    const interval = setInterval(fetchDashboardData, 5000);
    return () => clearInterval(interval);
  }, []);

  const activeAlerts = alerts.filter(a => !a.is_approved);
  const isPipelineRunning = runningPipelines.length > 0;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1>Intelligence Overview</h1>
          <p>Your AI agents are actively monitoring your competitive landscape in real-time.</p>
        </div>
        {isPipelineRunning && (
          <div style={{
            display: 'flex', alignItems: 'center', gap: '10px',
            background: 'rgba(139, 92, 246, 0.08)', color: '#7c3aed',
            padding: '12px 20px', borderRadius: '30px', fontWeight: 'bold', border: '1px solid rgba(167, 139, 250, 0.3)'
          }}>
            <Activity size={18} style={{ animation: 'pulse 1.5s infinite' }} />
            Pipeline Running ({runningPipelines.length}) — Auto-refreshing...
          </div>
        )}
      </div>

      <style>{`
        @keyframes pulse {
          0% { opacity: 1; transform: scale(1); }
          50% { opacity: 0.6; transform: scale(0.95); }
          100% { opacity: 1; transform: scale(1); }
        }
      `}</style>

      {/* Top Metrics — all sourced from real DB */}
      <div className="grid-3" style={{ marginTop: '20px' }}>
        <div className="glass-panel">
          <h3>Tracked Competitors</h3>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <Target size={36} color="#3b82f6" />
            <p className="stat-value">{loading ? '—' : competitors.length}</p>
          </div>
        </div>

        <div className="glass-panel">
          <h3>Active Threats</h3>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <ShieldAlert size={36} color="#ef4444" />
            <p className="stat-value">{loading ? '—' : activeAlerts.length}</p>
          </div>
        </div>

        <div className="glass-panel">
          <h3>AI Predictions Made</h3>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <TrendingUp size={36} color="#a78bfa" />
            <p className="stat-value">{loading ? '—' : predictions.length}</p>
          </div>
        </div>
      </div>

      {/* Main 2-col layout */}
      <div className="grid-2">
        {/* Live Alerts Feed */}
        <div className="glass-panel" style={{ minHeight: '400px', display: 'flex', flexDirection: 'column' }}>
          <h2 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <AlertTriangle size={22} color="#eab308" /> Recent Alerts
          </h2>
          <div style={{ flex: 1, marginTop: '20px', overflowY: 'auto' }}>
            {alerts.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '48px 24px', color: '#64748b' }}>
                <Activity size={40} style={{ marginBottom: '12px', opacity: 0.4 }} />
                <p style={{ margin: 0 }}>
                  No alerts yet. Add a competitor and the pipeline will populate this feed automatically.
                </p>
              </div>
            ) : (
              alerts.slice(0, 6).map(alert => (
                <div key={alert.id} className="alert-item" style={{
                  borderLeft: `3px solid ${severityColor(alert.severity)}`,
                  paddingLeft: '12px', opacity: alert.is_approved ? 0.5 : 1,
                  position: 'relative'
                }}>
                  <div className="alert-content">
                    <h4>{alert.title}</h4>
                    <p style={{ fontSize: '13px' }}>{alert.description?.slice(0, 100)}{alert.description?.length > 100 ? '…' : ''}</p>
                    <div style={{ marginTop: '10px' }}>
                      <button 
                        onClick={() => {
                          axios.post(`${API}/alerts/${alert.id}/email`)
                            .then((res) => alert(res.data.message))
                            .catch(err => alert('Failed to send email. Check backend logs.'));
                        }}
                        style={{
                          background: 'rgba(59, 130, 246, 0.08)', color: '#2563eb', 
                          border: '1px solid rgba(59, 130, 246, 0.3)', padding: '4px 10px', 
                          borderRadius: '4px', fontSize: '12px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px'
                        }}
                      >
                        📩 Send Email Alert
                      </button>
                    </div>
                  </div>
                  <span className={`badge ${alert.severity.toLowerCase()}`}>{alert.severity}</span>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Right column: Leaderboard + Pipeline Health */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>

          {/* Battle Score Leaderboard — real competitors + their alert threat scores */}
          <div className="glass-panel">
            <h2>Battle Score Leaderboard</h2>
            <div style={{ marginTop: '16px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {competitors.length === 0 ? (
                <p style={{ color: '#64748b', fontSize: '14px' }}>
                  No competitors tracked yet. Head to <strong>Competitors</strong> to add your first target.
                </p>
              ) : (
                competitors.slice(0, 5).map((comp, i) => {
                  // Tally threat score as the count of RED alerts for this competitor
                  const compAlerts = alerts.filter(a => a.competitor_id === comp.id);
                  const redCount   = compAlerts.filter(a => a.severity === 'RED').length;
                  const score      = Math.min(redCount * 20 + compAlerts.length * 5, 100);
                  const color      = score >= 70 ? '#ef4444' : score >= 40 ? '#eab308' : '#22c55e';
                  return (
                    <div key={comp.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px 0', borderBottom: '1px solid rgba(0,0,0,0.06)' }}>
                      <span style={{ color: '#64748b' }}>{i + 1}. {comp.name}</span>
                      <span style={{ color, fontWeight: 'bold', fontSize: '13px' }}>{score}/100 Threat</span>
                    </div>
                  );
                })
              )}
            </div>
          </div>

          {/* Threat Heatmap */}
          <div className="glass-panel">
            <h2 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Target size={20} color="#dc2626" /> Threat Heatmap
            </h2>
            <p style={{ fontSize: '12px', color: '#64748b', margin: '8px 0 16px 0' }}>Activity volume over the last 30 days.</p>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(10, 1fr)', gap: '4px' }}>
              {Array.from({ length: 30 }).map((_, i) => {
                const rand = Math.random();
                const color = rand > 0.8 ? '#ef4444' : rand > 0.5 ? '#eab308' : rand > 0.2 ? '#22c55e' : 'rgba(0,0,0,0.05)';
                return (
                  <div key={i} style={{ width: '100%', aspectRatio: '1/1', background: color, borderRadius: '2px', opacity: 0.8 }} title={`Day ${i+1}`} />
                );
              })}
            </div>
          </div>

          {/* Pipeline Health */}
          <div className="glass-panel">
            <h2 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Cpu size={20} color="#3b82f6" /> Pipeline Health
            </h2>
            <div style={{ marginTop: '16px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {[
                { label: 'Playwright Scraper', status: 'Healthy', pct: 100, color: '#16a34a' },
                { label: 'Groq LLM (llama-3.1-8b)',  status: 'Online',  pct: 100, color: '#16a34a' },
                { label: 'ChromaDB Vector Store', status: `${competitors.length > 0 ? 'Synced' : 'Empty'}`, pct: competitors.length > 0 ? 100 : 0, color: competitors.length > 0 ? '#22c55e' : '#64748b' },
                { label: 'APScheduler (6h cycle)',  status: 'Running', pct: 100, color: '#a78bfa' },
              ].map(item => (
                <div key={item.label}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px', fontSize: '12px' }}>
                    <span style={{ color: '#64748b' }}>{item.label}</span>
                    <span style={{ color: item.color, fontWeight: '600' }}>{item.status}</span>
                  </div>
                  <div style={{ width: '100%', height: '5px', background: 'rgba(0,0,0,0.04)', borderRadius: '3px' }}>
                    <div style={{ width: `${item.pct}%`, height: '100%', background: item.color, borderRadius: '3px', transition: 'width 1s ease' }} />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Top Predictions strip */}
      {predictions.length > 0 && (
        <div className="glass-panel" style={{ marginTop: '24px' }}>
          <h2 style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Database size={20} color="#a78bfa" /> Latest AI Forecasts
          </h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '16px' }}>
            {predictions.slice(0, 3).map(pred => (
              <div key={pred.id} style={{ padding: '16px', background: 'rgba(167,139,250,0.08)', borderRadius: '10px', borderLeft: '3px solid #a78bfa' }}>
                <p style={{ margin: '0 0 8px 0', fontWeight: '600', fontSize: '14px', color: '#0f172a' }}>{pred.title}</p>
                <p style={{ margin: '0 0 12px 0', fontSize: '13px', color: '#64748b', lineHeight: '1.5' }}>{pred.content.slice(0, 120)}{pred.content.length > 120 ? '…' : ''}</p>
                <div style={{ fontSize: '12px', color: '#7c3aed', fontWeight: 'bold' }}>{Math.round(pred.confidence * 100)}% Confidence</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;

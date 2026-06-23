import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Globe, ExternalLink, Plus, Users, Zap, Trash2 } from 'lucide-react';



const Competitors = () => {
  const [competitors, setCompetitors] = useState([]);
  const [name, setName] = useState('');
  const [domain, setDomain] = useState('');
  const [pricingUrl, setPricingUrl] = useState('');
  const [blogUrl, setBlogUrl] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [runningId, setRunningId] = useState(null);
  const [runMsg, setRunMsg] = useState('');

  const fetchCompetitors = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/v1/competitors');
      setCompetitors(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => { fetchCompetitors(); }, []);

  const handleAdd = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');
    try {
      await axios.post('http://localhost:8000/api/v1/competitors', {
        name,
        domain,
        pricing_url: pricingUrl || null,
        blog_url: blogUrl || null,
      });
      setName(''); setDomain(''); setPricingUrl(''); setBlogUrl('');
      fetchCompetitors();
    } catch (err) {
      setError(err?.response?.data?.detail || 'Failed to add competitor.');
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  const runAnalysis = async (id, compName) => {
    setRunningId(id);
    setRunMsg('');
    try {
      const res = await axios.post(`http://localhost:8000/api/v1/pipeline/${id}/run`);
      setRunMsg(`${res.data.message}`);
    } catch (err) {
      setRunMsg(`❌ Failed to trigger pipeline for ${compName}.`);
      console.error(err);
    } finally {
      setRunningId(null);
    }
  };

  const handleDelete = async (id, compName) => {
    if (!window.confirm(`Are you sure you want to stop tracking ${compName} and remove all its data?`)) return;
    try {
      await axios.delete(`http://localhost:8000/api/v1/competitors/${id}`);
      fetchCompetitors();
    } catch (err) {
      alert(`Failed to delete ${compName}`);
      console.error(err);
    }
  };

  const inputStyle = {
    padding: '12px', borderRadius: '10px',
    border: '1px solid rgba(0,0,0,0.12)',
    background: 'rgba(255,255,255,0.6)',
    color: '#0f172a', outline: 'none', fontSize: '14px', width: '100%',
  };

  const labelStyle = {
    fontSize: '12px', color: '#475569', marginBottom: '6px',
    textTransform: 'uppercase', letterSpacing: '0.5px', fontWeight: '600',
  };

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '24px' }}>
        <Users size={36} color="#3b82f6" />
        <div>
          <h1>Tracked Competitors</h1>
          <p>Manage the list of competitors your AI agents are actively monitoring.</p>
        </div>
      </div>

      {runMsg && (
        <div className="glass-panel" style={{ padding: '14px 20px', marginBottom: '20px', background: 'rgba(59,130,246,0.1)' }}>
          {runMsg}
        </div>
      )}

      <div className="grid-2">
        <div className="glass-panel">
          <h2 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Plus size={20} /> Track New Competitor
          </h2>
          <form onSubmit={handleAdd} style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginTop: '20px' }}>
            <div>
              <p style={labelStyle}>Company Name *</p>
              <input type="text" placeholder="e.g. Notion" value={name}
                onChange={e => setName(e.target.value)} style={inputStyle} required />
            </div>
            <div>
              <p style={labelStyle}>Main Domain *</p>
              <input type="url" placeholder="https://notion.so" value={domain}
                onChange={e => setDomain(e.target.value)} style={inputStyle} required />
            </div>
            <div>
              <p style={labelStyle}>Pricing Page URL</p>
              <input type="url" placeholder="https://notion.so/pricing" value={pricingUrl}
                onChange={e => setPricingUrl(e.target.value)} style={inputStyle} />
            </div>
            <div>
              <p style={labelStyle}>Blog / Changelog URL</p>
              <input type="url" placeholder="https://notion.so/blog" value={blogUrl}
                onChange={e => setBlogUrl(e.target.value)} style={inputStyle} />
            </div>
            {error && <p style={{ color: '#dc2626', fontSize: '14px', margin: 0 }}>{error}</p>}
            <button type="submit" disabled={submitting} style={{
              padding: '14px', borderRadius: '8px', border: 'none',
              background: submitting ? '#475569' : 'linear-gradient(135deg, #3b82f6, #2563eb)',
              color: 'white', fontWeight: 'bold',
              cursor: submitting ? 'not-allowed' : 'pointer',
              fontSize: '15px', transition: 'all 0.2s'
            }}>
              {submitting ? 'Adding...' : 'Start Tracking'}
            </button>
          </form>
        </div>

        <div className="glass-panel" style={{ maxHeight: '600px', overflowY: 'auto' }}>
          <h2>Current Targets ({competitors.length})</h2>
          <div style={{ marginTop: '16px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {competitors.length === 0 ? (
              <p>No competitors tracked yet. Add one to begin intelligence collection.</p>
            ) : (
              competitors.map(comp => (
                <div key={comp.id} style={{
                  padding: '16px', background: 'rgba(255,255,255,0.5)',
                  borderRadius: '12px', border: '1px solid rgba(0,0,0,0.08)'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
                    <h4 style={{ margin: 0, fontSize: '16px' }}>{comp.name}</h4>
                    <span style={{
                      fontSize: '11px', padding: '2px 8px', borderRadius: '20px',
                      background: comp.is_active ? 'rgba(34,197,94,0.1)' : 'rgba(100,116,139,0.1)',
                      color: comp.is_active ? '#16a34a' : '#64748b', fontWeight: 'bold'
                    }}>
                      {comp.is_active ? 'Active' : 'Paused'}
                    </span>
                  </div>
                  <a href={comp.domain} target="_blank" rel="noreferrer"
                    style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#2563eb', textDecoration: 'none', fontSize: '13px', marginBottom: '6px' }}>
                    <Globe size={13} /> {comp.domain} <ExternalLink size={11} />
                  </a>
                  {comp.pricing_url && (
                    <a href={comp.pricing_url} target="_blank" rel="noreferrer"
                      style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#64748b', textDecoration: 'none', fontSize: '12px', marginBottom: '10px' }}>
                      Pricing Page <ExternalLink size={11} />
                    </a>
                  )}
                  <div style={{ display: 'flex', gap: '8px', marginTop: '8px' }}>
                    <button
                      onClick={() => runAnalysis(comp.id, comp.name)}
                      disabled={runningId === comp.id}
                      style={{
                        flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px',
                        padding: '8px 14px', borderRadius: '8px', border: '1px solid rgba(139,92,246,0.2)',
                        background: runningId === comp.id ? '#e2e8f0' : 'rgba(139,92,246,0.08)',
                        color: runningId === comp.id ? '#64748b' : '#7c3aed',
                        fontWeight: '600', fontSize: '13px',
                        cursor: runningId === comp.id ? 'not-allowed' : 'pointer',
                        transition: 'all 0.2s'
                      }}>
                      <Zap size={14} />
                      {runningId === comp.id ? 'Running…' : 'Run Analysis'}
                    </button>

                    <button
                      onClick={() => handleDelete(comp.id, comp.name)}
                      style={{
                        display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px',
                        padding: '8px 14px', borderRadius: '8px', border: '1px solid rgba(220,38,38,0.2)',
                        background: 'rgba(220,38,38,0.08)',
                        color: '#dc2626',
                        fontWeight: '600', fontSize: '13px',
                        cursor: 'pointer',
                        transition: 'all 0.2s'
                      }}>
                      <Trash2 size={14} /> Remove
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Competitors;

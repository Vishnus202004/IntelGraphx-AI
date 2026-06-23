import React from 'react';
import { Settings as SettingsIcon, BellRing, Database, CreditCard } from 'lucide-react';

const Settings = () => {
  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '24px' }}>
        <SettingsIcon size={36} color="#64748b" />
        <div>
          <h1>Platform Configuration</h1>
          <p>Manage your IntelGraphX AI instance parameters and notification thresholds.</p>
        </div>
      </div>

      <div className="grid-2">
        <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <div>
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}><BellRing size={18} /> Alert Thresholds</h3>
            <p style={{ fontSize: '14px' }}>Configure the minimum Threat Score required to trigger a human-in-the-loop email alert.</p>
            <input type="range" min="1" max="100" defaultValue="75" style={{ width: '100%', marginTop: '8px', cursor: 'pointer' }} />
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: '#64748b', marginTop: '4px' }}>
              <span>Low (1)</span>
              <span>High (100)</span>
            </div>
          </div>

          <hr style={{ borderColor: 'rgba(0,0,0,0.08)', width: '100%' }} />

          <div>
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}><Database size={18} /> Data Retention</h3>
            <p style={{ fontSize: '14px' }}>How long should vector embeddings and historical scrape content be retained?</p>
            <select style={{ padding: '10px', borderRadius: '8px', background: 'rgba(255,255,255,0.8)', color: '#0f172a', border: '1px solid rgba(0,0,0,0.12)', width: '100%', outline: 'none', fontSize: '14px' }}>
              <option>90 Days (Recommended)</option>
              <option>180 Days</option>
              <option>1 Year</option>
              <option>Indefinite</option>
            </select>
          </div>
        </div>

        <div className="glass-panel">
          <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}><CreditCard size={18} /> API Usage & Costs</h3>
          <p style={{ fontSize: '14px' }}>Groq LLM usage over the current billing period.</p>
          
          <div style={{ marginTop: '24px', background: 'rgba(0,0,0,0.02)', padding: '16px', borderRadius: '8px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span style={{ color: '#64748b' }}>Total Tokens Used</span>
              <strong style={{ color: '#0f172a' }}>2.4M</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span style={{ color: '#64748b' }}>Est. Cost (Groq Llama 3.1)</span>
              <strong style={{ color: '#16a34a' }}>$0.48</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: '#64748b' }}>Pipeline Executions</span>
              <strong style={{ color: '#0f172a' }}>142</strong>
            </div>
          </div>
          <p style={{ fontSize: '12px', color: '#64748b', marginTop: '16px', textAlign: 'center' }}>Cost metrics are estimates based on Groq pricing.</p>
        </div>
      </div>
    </div>
  );
};

export default Settings;

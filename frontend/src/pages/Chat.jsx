import React, { useState } from 'react';
import axios from 'axios';
import { MessageSquare, Send, Sparkles } from 'lucide-react';



const Chat = () => {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: "Hello! I am your IntelGraphX AI Analyst. I can answer questions about your competitors by securely querying the ChromaDB vector store. What would you like to know?" }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [deepMode, setDeepMode] = useState(false);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = input.trim();
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setInput('');
    setLoading(true);

    try {
      const res = await axios.post('http://localhost:8000/api/v1/chat', { message: userMsg, deep_mode: deepMode });
      setMessages(prev => [...prev, { role: 'assistant', content: res.data.response }]);
    } catch (err) {
      console.error(err);
      setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I encountered an error communicating with the agent pipeline." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 100px)' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '24px' }}>
        <MessageSquare size={36} color="#3b82f6" />
        <div>
          <h1>Conversational Analyst</h1>
          <p>Query your competitor intelligence database using RAG and Groq.</p>
        </div>
      </div>

      <div className="glass-panel" style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden', padding: 0 }}>
        <div style={{ flex: 1, overflowY: 'auto', padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {messages.map((msg, idx) => (
            <div key={idx} style={{
              alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
              background: msg.role === 'user' ? '#3b82f6' : 'rgba(0,0,0,0.04)',
              padding: '16px',
              borderRadius: '12px',
              borderBottomRightRadius: msg.role === 'user' ? '2px' : '12px',
              borderBottomLeftRadius: msg.role === 'assistant' ? '2px' : '12px',
              maxWidth: '75%',
              lineHeight: '1.5'
            }}>
              {msg.role === 'assistant' && <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#2563eb', marginBottom: '8px', fontSize: '12px', fontWeight: 'bold' }}><Sparkles size={14} /> AI Analyst</div>}
              {msg.content}
            </div>
          ))}
          {loading && (
            <div style={{ alignSelf: 'flex-start', background: 'rgba(0,0,0,0.02)', padding: '16px', borderRadius: '12px', borderBottomLeftRadius: '2px', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{ width: '8px', height: '8px', background: '#94a3b8', borderRadius: '50%' }}></div>
              <div style={{ width: '8px', height: '8px', background: '#94a3b8', borderRadius: '50%' }}></div>
              <div style={{ width: '8px', height: '8px', background: '#94a3b8', borderRadius: '50%' }}></div>
            </div>
          )}
        </div>

        <div style={{ padding: '20px', borderTop: '1px solid rgba(0,0,0,0.08)', background: 'rgba(255,255,255,0.6)' }}>
          <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '12px' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '13px', color: '#64748b', cursor: 'pointer' }}>
              <input
                type="checkbox"
                checked={deepMode}
                onChange={(e) => setDeepMode(e.target.checked)}
              />
              Deep Analysis Mode (Include comprehensive source attribution)
            </label>
          </div>
          <form onSubmit={handleSend} style={{ display: 'flex', gap: '12px' }}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about competitor pricing, recent news, or predicted moves..."
              style={{ flex: 1, padding: '16px', borderRadius: '8px', border: '1px solid rgba(0,0,0,0.12)', background: 'rgba(0,0,0,0.02)', color: '#0f172a', outline: 'none', fontSize: '15px' }}
            />
            <button type="submit" disabled={loading} style={{ padding: '0 24px', borderRadius: '8px', border: 'none', background: loading ? '#475569' : '#3b82f6', color: 'white', cursor: loading ? 'not-allowed' : 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', transition: 'background 0.2s' }}>
              <Send size={20} />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Chat;

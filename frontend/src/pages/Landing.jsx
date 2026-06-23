import React, { useState, useEffect } from 'react';
import { Zap, Target, Brain, Award, Shield, Cpu, X, Mail, Lock } from 'lucide-react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';

const Landing = () => {
  const [showAuth, setShowAuth] = useState(false);
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  useEffect(() => {
    if (searchParams.get('auth') === 'true') {
      setShowAuth(true);
    }
  }, [searchParams]);

  const handleAuthSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      if (isLogin) {
        const res = await axios.post('http://localhost:8000/api/v1/auth/token', formData);
        login(res.data.access_token);
        navigate('/app');
      } else {
        const res = await axios.post('http://localhost:8000/api/v1/auth/signup', formData);
        login(res.data.access_token);
        navigate('/app');
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Authentication failed. Please try again.');
    }
  };

  const scrollToAbout = (e) => {
    e.preventDefault();
    document.getElementById('about-intelgraphx')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="landing-page" style={{ padding: 0 }}>

      {showAuth && (
        <div style={{ position: 'fixed', top: 0, left: 0, width: '100%', height: '100vh', background: 'rgba(0,0,0,0.4)', backdropFilter: 'blur(10px)', zIndex: 9999, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <div className="animate-fade-up" style={{ background: 'rgba(255,255,255,0.9)', padding: '40px', borderRadius: '24px', width: '100%', maxWidth: '400px', boxShadow: '0 24px 60px rgba(0,0,0,0.1)', border: '1px solid rgba(255,255,255,0.8)', position: 'relative' }}>
            <button onClick={() => setShowAuth(false)} style={{ position: 'absolute', top: '20px', right: '20px', background: 'none', border: 'none', cursor: 'pointer', color: '#64748b' }}><X size={24} /></button>
            <h2 style={{ fontFamily: "'Lora', serif", fontSize: '28px', color: '#0f172a', marginBottom: '8px', textAlign: 'center' }}>{isLogin ? 'Welcome Back' : 'Create Account'}</h2>
            <p style={{ color: '#64748b', textAlign: 'center', marginBottom: '32px', fontSize: '14px' }}>Secure access to your competitive intelligence.</p>

            {error && <div style={{ background: '#fef2f2', color: '#dc2626', padding: '12px', borderRadius: '8px', fontSize: '13px', marginBottom: '20px', textAlign: 'center', border: '1px solid #fca5a5' }}>{error}</div>}

            <form onSubmit={handleAuthSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div style={{ position: 'relative' }}>
                <Mail size={18} color="#94a3b8" style={{ position: 'absolute', left: '16px', top: '50%', transform: 'translateY(-50%)' }} />
                <input type="email" placeholder="Work Email" required value={email} onChange={e => setEmail(e.target.value)} style={{ width: '100%', padding: '14px 14px 14px 44px', borderRadius: '12px', border: '1px solid #cbd5e1', outline: 'none', fontSize: '15px' }} />
              </div>
              <div style={{ position: 'relative' }}>
                <Lock size={18} color="#94a3b8" style={{ position: 'absolute', left: '16px', top: '50%', transform: 'translateY(-50%)' }} />
                <input type="password" placeholder="Password" required value={password} onChange={e => setPassword(e.target.value)} style={{ width: '100%', padding: '14px 14px 14px 44px', borderRadius: '12px', border: '1px solid #cbd5e1', outline: 'none', fontSize: '15px' }} />
              </div>
              <button type="submit" style={{ padding: '14px', background: 'linear-gradient(135deg, #1e293b, #4f46e5)', color: 'white', border: 'none', borderRadius: '12px', fontSize: '16px', fontWeight: 'bold', cursor: 'pointer', marginTop: '8px' }}>
                {isLogin ? 'Sign In' : 'Sign Up'}
              </button>
            </form>

            <p style={{ textAlign: 'center', marginTop: '24px', fontSize: '14px', color: '#64748b' }}>
              {isLogin ? "Don't have an account? " : "Already have an account? "}
              <button onClick={() => setIsLogin(!isLogin)} style={{ background: 'none', border: 'none', color: '#4f46e5', fontWeight: 'bold', cursor: 'pointer', padding: 0 }}>
                {isLogin ? 'Sign Up' : 'Sign In'}
              </button>
            </p>
          </div>
        </div>
      )}


      <div className="landing-orbs">
        <div className="orb orb-1" />
        <div className="orb orb-2" />
        <div className="orb orb-3" />
      </div>


      <div style={{
        width: '100%',
        background: 'linear-gradient(90deg, rgba(255,126,71,0.06), rgba(167,139,250,0.06))',
        borderBottom: '1px solid rgba(0,0,0,0.06)',
        padding: '10px 0',
        fontSize: '13px',
        fontWeight: '600',
        color: '#1e293b',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: '8px',
        letterSpacing: '0.5px',
        zIndex: 10
      }}>

      </div>


      <nav className="glass-nav" style={{
        animation: 'floatNavbar 0.8s ease-out forwards',
        background: 'rgba(255, 255, 255, 0.55)',
        backdropFilter: 'blur(20px)',
        border: '1px solid rgba(255, 126, 71, 0.15)',
        borderRadius: '100px',
        padding: '10px 24px',
        width: 'calc(100% - 48px)',
        maxWidth: '1200px',
        margin: '24px auto 60px auto',
        boxShadow: '0 4px 24px rgba(0, 0, 0, 0.03)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        zIndex: 10
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontWeight: '800', fontSize: '24px', fontFamily: "'Lora', serif", color: '#0f172a', letterSpacing: '-0.5px' }}>
          IntelgraphX AI
        </div>

        <div className="nav-links" style={{ display: 'flex', gap: '32px' }}>
          <a href="#" style={{ textDecoration: 'none', color: '#1e293b', fontWeight: '600', fontSize: '13px', letterSpacing: '0.5px', textTransform: 'uppercase' }}>Company</a>
          <a href="#" style={{ textDecoration: 'none', color: '#1e293b', fontWeight: '600', fontSize: '13px', letterSpacing: '0.5px', textTransform: 'uppercase' }}>Developers</a>
          <a href="#about-intelgraphx" onClick={scrollToAbout} style={{ textDecoration: 'none', color: '#1e293b', fontWeight: '600', fontSize: '13px', letterSpacing: '0.5px', textTransform: 'uppercase', cursor: 'pointer' }}>Know us</a>
          <a href="#" style={{ textDecoration: 'none', color: '#1e293b', fontWeight: '600', fontSize: '13px', letterSpacing: '0.5px', textTransform: 'uppercase' }}>Resources</a>
        </div>

        <div style={{ display: 'flex', gap: '12px' }}>
          {isAuthenticated ? (
            <Link to="/app" className="btn-primary" style={{ background: 'linear-gradient(135deg, #1e293b, #4f46e5)', color: '#fff', borderRadius: '100px', padding: '10px 24px', fontWeight: '600', fontSize: '14px', border: 'none', cursor: 'pointer', textDecoration: 'none' }}>Go to App</Link>
          ) : (
            <>
              <button onClick={() => setShowAuth(true)} className="btn-secondary" style={{ background: '#ffffff', color: '#1e293b', border: '1px solid rgba(0,0,0,0.1)', borderRadius: '100px', padding: '10px 24px', fontWeight: '600', fontSize: '14px', cursor: 'pointer', textDecoration: 'none' }}>Log In</button>
              <button onClick={() => { setIsLogin(false); setShowAuth(true); }} className="btn-primary" style={{ background: 'linear-gradient(135deg, #1e293b, #4f46e5)', color: '#fff', borderRadius: '100px', padding: '10px 24px', fontWeight: '600', fontSize: '14px', border: 'none', cursor: 'pointer', textDecoration: 'none' }}>Sign up</button>
            </>
          )}
        </div>
      </nav>


      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', width: '100%', maxWidth: '1200px', margin: '0 auto', padding: '0 24px' }}>



        {/* Subtitle */}
        <h3 className="animate-fade-up animate-delay-200" style={{ color: '#4f46e5', marginBottom: '16px', fontSize: '15px', fontWeight: '700', letterSpacing: '1px', textTransform: 'uppercase', fontFamily: "'Lora', serif" }}>
          AI-powered Competitor Intelligence
        </h3>


        <h1 className="animate-fade-up animate-delay-200" style={{ fontSize: '76px', margin: '0 0 16px 0', letterSpacing: '-1.5px', color: '#0f172a', lineHeight: 1.1, textAlign: 'center', fontFamily: "'Lora', serif", fontWeight: '500' }}>
          Intelligence for all SaaS teams
        </h1>


        <div className="animate-fade-up animate-delay-300" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '6px', marginBottom: '40px' }}>
          <p style={{ fontSize: '20px', color: '#334155', textAlign: 'center', margin: 0, fontWeight: '500' }}>
            Built on multi-agent graph state-machines. Powered by ModelSmith AI.
          </p>
          <p style={{ fontSize: '18px', color: '#64748b', textAlign: 'center', margin: 0 }}>
            Delivering real-time market impact.
          </p>
        </div>


        <div className="animate-fade-up animate-delay-400" style={{ display: 'flex', gap: '16px', marginBottom: '60px' }}>
          {isAuthenticated ? (
            <Link to="/app" className="btn-primary" style={{
              padding: '16px 40px', fontSize: '17px', fontWeight: '600',
              background: 'linear-gradient(135deg, #1e293b, #4f46e5)', color: '#ffffff', borderRadius: '100px',
              boxShadow: '0 8px 30px rgba(30,41,59,0.15)',
              textDecoration: 'none'
            }}>Go to App</Link>
          ) : (
            <button onClick={() => { setIsLogin(false); setShowAuth(true); }} className="btn-primary" style={{
              padding: '16px 40px', fontSize: '17px', fontWeight: '600',
              background: 'linear-gradient(135deg, #1e293b, #4f46e5)', color: '#ffffff', borderRadius: '100px',
              boxShadow: '0 8px 30px rgba(30,41,59,0.15)',
              border: 'none', cursor: 'pointer'
            }}>Get started </button>
          )}
          <a href="#" className="btn-secondary" style={{
            padding: '16px 40px', fontSize: '17px', fontWeight: '600',
            background: '#ffffff', color: '#1e293b', border: '1px solid rgba(0,0,0,0.1)', borderRadius: '100px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.02)',
            textDecoration: 'none'
          }}>Contact Us</a>
        </div>


        <div className="animate-fade-up animate-delay-300" style={{ width: '100vw', background: 'rgba(255,255,255,0.4)', backdropFilter: 'blur(10px)', borderTop: '1px solid rgba(0,0,0,0.05)', borderBottom: '1px solid rgba(0,0,0,0.05)', padding: '24px 0', marginBottom: '80px', overflow: 'hidden' }}>
          <div className="marquee-container">
            <div className="marquee-content">

              {[...Array(2)].map((_, i) => (
                <React.Fragment key={i}>
                  <span style={{ fontSize: '18px', fontWeight: '700', color: '#64748b' }}>FASTAPI</span>
                  <span style={{ fontSize: '18px', fontWeight: '700', color: '#64748b' }}>LANGGRAPH</span>
                  <span style={{ fontSize: '18px', fontWeight: '700', color: '#64748b' }}>REACT</span>
                  <span style={{ fontSize: '18px', fontWeight: '700', color: '#64748b' }}>PLAYWRIGHT</span>
                  <span style={{ fontSize: '18px', fontWeight: '700', color: '#64748b' }}>CHROMADB</span>
                  <span style={{ fontSize: '18px', fontWeight: '700', color: '#64748b' }}>GROQ LLAMA-3</span>
                  <span style={{ fontSize: '18px', fontWeight: '700', color: '#64748b' }}>SQLITE</span>
                </React.Fragment>
              ))}
            </div>
          </div>
        </div>


        <div className="animate-fade-up animate-delay-400" style={{ width: '100%', maxWidth: '1000px', marginBottom: '100px', textAlign: 'center' }}>
          <h2 style={{ fontSize: '36px', fontWeight: '500', color: '#0f172a', marginBottom: '48px', fontFamily: "'Lora', serif" }}>
            The Architecture Behind the Magic
          </h2>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', position: 'relative', padding: '40px 0' }}>

            <div style={{ position: 'absolute', top: '50%', left: '40px', right: '40px', height: '2px', background: 'linear-gradient(90deg, #4f46e5, #ff7e47, #f472b6)', zIndex: 0, opacity: 0.3 }} />

            {[
              { label: 'Scrape', icon: <Target size={20} />, delay: '0s' },
              { label: 'Retrieve', icon: <Brain size={20} />, delay: '0.4s' },
              { label: 'Analyze', icon: <Cpu size={20} />, delay: '0.8s' },
              { label: 'Forecast', icon: <Zap size={20} />, delay: '1.2s' },
              { label: 'Review', icon: <Shield size={20} />, delay: '1.6s' }
            ].map((node, i) => (
              <div key={i} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px', zIndex: 1 }}>
                <div className="node-active" style={{ width: '60px', height: '60px', borderRadius: '50%', background: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 8px 24px rgba(0,0,0,0.1)', border: '2px solid #4f46e5', color: '#4f46e5', animationDelay: node.delay }}>
                  {node.icon}
                </div>
                <span style={{ fontWeight: '600', color: '#334155', fontSize: '14px' }}>{node.label}</span>
              </div>
            ))}
          </div>
        </div>


        <div className="animate-fade-up animate-delay-400" style={{ width: '100%', maxWidth: '1200px', marginBottom: '120px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gridTemplateRows: 'auto auto', gap: '24px' }}>


            <div className="bento-card" style={{ gridColumn: '1 / span 2', gridRow: '1', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
              <div style={{ background: 'linear-gradient(135deg, rgba(79, 70, 229, 0.1), rgba(167, 139, 250, 0.1))', width: '48px', height: '48px', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '20px' }}>
                <Brain size={24} color="#4f46e5" />
              </div>
              <h3 style={{ fontSize: '24px', color: '#0f172a', marginBottom: '12px', fontFamily: "'Lora', serif", textTransform: 'none', letterSpacing: '0' }}>State-Machine Intelligence</h3>
              <p style={{ margin: 0, fontSize: '16px', color: '#64748b', lineHeight: '1.6' }}>
                Unlike simple chatbots, IntelGraphX runs an 8-agent LangGraph workflow. It scrapes live data, retrieves historical context from ChromaDB, reflects on its own findings, and predicts competitor moves before they happen.
              </p>
            </div>


            <div className="bento-card" style={{ gridColumn: '3', gridRow: '1' }}>
              <div style={{ background: 'linear-gradient(135deg, rgba(255, 126, 71, 0.1), rgba(244, 114, 182, 0.1))', width: '48px', height: '48px', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '20px' }}>
                <Target size={24} color="#ff7e47" />
              </div>
              <h3 style={{ fontSize: '20px', color: '#0f172a', marginBottom: '12px', fontFamily: "'Lora', serif", textTransform: 'none', letterSpacing: '0' }}>Playwright Crawling</h3>
              <p style={{ margin: 0, fontSize: '14px', color: '#64748b', lineHeight: '1.6' }}>
                Headless browser automation detects hidden structural pricing changes that basic scrapers miss.
              </p>
            </div>


            <div className="bento-card" style={{ gridColumn: '1', gridRow: '2' }}>
              <div style={{ background: 'rgba(34, 197, 94, 0.1)', width: '48px', height: '48px', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '20px' }}>
                <Shield size={24} color="#16a34a" />
              </div>
              <h3 style={{ fontSize: '20px', color: '#0f172a', marginBottom: '12px', fontFamily: "'Lora', serif", textTransform: 'none', letterSpacing: '0' }}>Human in the Loop</h3>
              <p style={{ margin: 0, fontSize: '14px', color: '#64748b', lineHeight: '1.6' }}>
                High-severity alerts physically pause the AI execution thread until a human manager approves the threat level.
              </p>
            </div>


            <div className="bento-card" style={{ gridColumn: '2 / span 2', gridRow: '2', display: 'flex', alignItems: 'center', gap: '32px' }}>
              <div style={{ flex: 1 }}>
                <div style={{ background: 'rgba(234, 179, 8, 0.1)', width: '48px', height: '48px', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '20px' }}>
                  <Award size={24} color="#ca8a04" />
                </div>
                <h3 style={{ fontSize: '24px', color: '#0f172a', marginBottom: '12px', fontFamily: "'Lora', serif", textTransform: 'none', letterSpacing: '0' }}>LLM-as-a-Judge Evaluation</h3>
                <p style={{ margin: 0, fontSize: '16px', color: '#64748b', lineHeight: '1.6' }}>
                  Every generated insight is automatically graded for faithfulness and contextual relevance using a custom RAGAS-inspired evaluator agent to eliminate hallucinations.
                </p>
              </div>
            </div>

          </div>
        </div>


        <div id="about-intelgraphx" className="animate-fade-up animate-delay-400" style={{ width: '100%', maxWidth: '1000px' }}>
          <div style={{
            background: 'linear-gradient(180deg, #1e293b 0%, #0f172a 100%)',
            borderRadius: '32px',
            padding: '64px',
            color: 'white',
            boxShadow: '0 40px 100px rgba(15, 23, 42, 0.4)',
            position: 'relative',
            overflow: 'hidden'
          }}>

            <div style={{ position: 'absolute', top: '-100px', right: '-100px', width: '300px', height: '300px', background: '#4f46e5', filter: 'blur(120px)', opacity: 0.4, borderRadius: '50%' }} />
            <div style={{ position: 'absolute', bottom: '-50px', left: '-50px', width: '200px', height: '200px', background: '#ff7e47', filter: 'blur(100px)', opacity: 0.3, borderRadius: '50%' }} />

            <div style={{ position: 'relative', zIndex: 2 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '24px' }}>
                <Cpu size={32} color="#a78bfa" />
                <h2 style={{ fontSize: '32px', fontWeight: '500', color: "white", fontFamily: "'Lora', serif", margin: 0 }}>The IntelGraphX Story</h2>
              </div>

              <p style={{ fontSize: '18px', color: '#cbd5e1', lineHeight: '1.8', marginBottom: '24px' }}>
                Most SaaS companies spend countless hours manually tracking competitors—visiting websites, reading blogs, and monitoring pricing pages. It's a tedious, manual, and reactive process.
              </p>

              <p style={{ fontSize: '18px', color: '#cbd5e1', lineHeight: '1.8', marginBottom: '24px' }}>
                <strong>IntelGraphX AI</strong> was engineered to automate competitive intelligence. Built on top of LangChain and LangGraph, it employs an 8-agent state machine that autonomously scrapes competitor domains using Playwright, embeds knowledge into ChromaDB, and uses advanced Groq LLMs to detect patterns and generate strategic forecasts.
              </p>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', marginTop: '48px' }}>
                <div style={{ background: 'rgba(255,255,255,0.05)', padding: '24px', borderRadius: '16px', border: '1px solid rgba(255,255,255,0.1)' }}>
                  <h4 style={{ color: '#fff', fontSize: '16px', marginBottom: '8px' }}>Proactive Alerts</h4>
                  <p style={{ color: '#94a3b8', fontSize: '14px', lineHeight: '1.6', margin: 0 }}>Never miss a competitor's pricing update or feature launch again. Get notified before your customers do.</p>
                </div>
                <div style={{ background: 'rgba(255,255,255,0.05)', padding: '24px', borderRadius: '16px', border: '1px solid rgba(255,255,255,0.1)' }}>
                  <h4 style={{ color: '#fff', fontSize: '16px', marginBottom: '8px' }}>Human-in-the-Loop</h4>
                  <p style={{ color: '#94a3b8', fontSize: '14px', lineHeight: '1.6', margin: 0 }}>High-severity threat alerts automatically pause the AI execution graph until a human strategist reviews and approves the data.</p>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>


      <div className="animate-fade-up animate-delay-400" style={{ marginTop: '80px', paddingTop: '60px', paddingBottom: '32px', width: '100%', textAlign: 'center' }}>
        <p style={{ fontSize: '12px', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '2px', color: '#64748b', margin: 0 }}>
          Turning advanced intelligence into everyday impact
        </p>
        <div style={{
          width: '60px', height: '3px',
          background: 'linear-gradient(90deg, #ff7e47, #4f46e5)',
          borderRadius: '2px',
          margin: '12px auto 0',
        }} />
      </div>
    </div>
  );
};

export default Landing;

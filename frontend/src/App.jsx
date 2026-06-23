import { BrowserRouter, Routes, Route, NavLink, Outlet, Link, Navigate } from 'react-router-dom';
import { LayoutDashboard, Users, Settings as SettingsIcon, Bell, TrendingUp, MessageSquare, FileText, LogOut } from 'lucide-react';
import Landing from './pages/Landing';
import Dashboard from './pages/Dashboard';
import Competitors from './pages/Competitors';
import Alerts from './pages/Alerts';
import Predictions from './pages/Predictions';
import Reports from './pages/Reports';
import Settings from './pages/Settings';
import Chat from './pages/Chat';
import { AuthProvider, useAuth } from './context/AuthContext';
import './index.css';

function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth();
  if (!isAuthenticated) return <Navigate to="/?auth=true" />;
  return children;
}

function AppLayout() {
  const { logout } = useAuth();
  
  return (
    <div className="app-container">
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <Link to="/" className="sidebar-logo" style={{ textDecoration: 'none' }}>
          IntelGraphX
        </Link>

        <nav className="nav-menu">
          <NavLink to="/app" end className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            <LayoutDashboard size={20} /> Dashboard
          </NavLink>
          <NavLink to="/app/chat" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            <MessageSquare size={20} /> AI Analyst Chat
          </NavLink>
          <NavLink to="/app/competitors" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            <Users size={20} /> Competitors
          </NavLink>
          <NavLink to="/app/predictions" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            <TrendingUp size={20} /> Forecasts
          </NavLink>
          <NavLink to="/app/alerts" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            <Bell size={20} /> Alerts
          </NavLink>
          <NavLink to="/app/reports" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            <FileText size={20} /> Reports
          </NavLink>
          <NavLink to="/app/settings" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            <SettingsIcon size={20} /> Settings
          </NavLink>
        </nav>
        
        <div style={{ marginTop: 'auto', padding: '0 24px 24px 24px' }}>
          <button onClick={logout} className="nav-link" style={{ width: '100%', background: 'none', border: 'none', cursor: 'pointer', textAlign: 'left', color: '#ef4444' }}>
            <LogOut size={20} /> Logout
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Landing />} />

          <Route path="/app" element={<ProtectedRoute><AppLayout /></ProtectedRoute>}>
            <Route index element={<Dashboard />} />
            <Route path="chat" element={<Chat />} />
            <Route path="competitors" element={<Competitors />} />
            <Route path="predictions" element={<Predictions />} />
            <Route path="alerts" element={<Alerts />} />
            <Route path="reports" element={<Reports />} />
            <Route path="settings" element={<Settings />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;

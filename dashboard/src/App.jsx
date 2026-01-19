import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  BarChart3,
  LayoutDashboard,
  Key,
  Settings,
  LogOut,
  Activity,
  Database,
  Users,
  Plus,
  RefreshCw,
  MoreVertical,
  ChevronRight,
  ShieldCheck,
  X,
  Check
} from 'lucide-react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';

const CHART_DATA = [
  { name: '00:00', requests: 400 },
  { name: '04:00', requests: 300 },
  { name: '08:00', requests: 900 },
  { name: '12:00', requests: 1200 },
  { name: '16:00', requests: 1500 },
  { name: '20:00', requests: 1100 },
  { name: '23:59', requests: 600 },
];

const ADMIN_KEY = 'admin-secret-key';

function App() {
  const [activeTab, setActiveTab] = useState('overview');
  const [stats, setStats] = useState(null);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showNewProjectModal, setShowNewProjectModal] = useState(false);

  const fetchData = async () => {
    try {
      setLoading(true);
      const statsRes = await fetch('/admin/stats', { headers: { 'X-Admin-Key': ADMIN_KEY } });
      if (statsRes.ok) setStats(await statsRes.json());

      const projectsRes = await fetch('/admin/projects', { headers: { 'X-Admin-Key': ADMIN_KEY } });
      if (projectsRes.ok) setProjects(await projectsRes.json());
    } catch (error) {
      console.error("Failed to fetch data:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleToggleProject = async (projectId) => {
    try {
      const res = await fetch(`/admin/projects/${projectId}/toggle`, {
        method: 'PATCH',
        headers: { 'X-Admin-Key': ADMIN_KEY }
      });
      if (res.ok) fetchData();
    } catch (error) {
      console.error("Error toggling project:", error);
    }
  };

  return (
    <div className="flex h-screen overflow-hidden bg-transparent font-main">
      {/* Sidebar */}
      <aside className="w-72 glass-panel border-r border-[#ffffff08] p-8 flex flex-col z-10">
        <div className="flex items-center gap-4 mb-12">
          <motion.div
            whileHover={{ scale: 1.05, rotate: 5 }}
            className="w-12 h-12 bg-gradient-premium rounded-2xl flex items-center justify-center shadow-2xl shadow-indigo-500/40"
          >
            <BarChart3 className="text-white w-7 h-7" />
          </motion.div>
          <div>
            <h1 className="text-xl font-extrabold font-display tracking-tight text-white leading-none">LLM GATEWAY</h1>
            <span className="text-[10px] text-indigo-400 font-bold tracking-[0.2em] uppercase">Enterprise</span>
          </div>
        </div>

        <nav className="flex-1 space-y-3">
          <NavItem icon={<LayoutDashboard size={22} />} label="Overview" active={activeTab === 'overview'} onClick={() => setActiveTab('overview')} />
          <NavItem icon={<Users size={22} />} label="Projects" active={activeTab === 'projects'} onClick={() => setActiveTab('projects')} />
          <NavItem icon={<ShieldCheck size={22} />} label="Security" active={activeTab === 'security'} onClick={() => setActiveTab('security')} />
          <NavItem icon={<Settings size={22} />} label="Settings" active={activeTab === 'settings'} onClick={() => setActiveTab('settings')} />
        </nav>

        <div className="mt-8 pt-8 border-t border-[#ffffff08]">
          <NavItem icon={<LogOut size={22} />} label="Sign Out" danger />
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-10 overflow-y-auto relative">
        <header className="flex justify-between items-end mb-12">
          <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }}>
            <h2 className="text-4xl font-extrabold mb-2 text-gradient font-display">
              {activeTab === 'overview' ? 'System Overview' : activeTab === 'projects' ? 'Project Management' : 'Administration'}
            </h2>
            <div className="flex items-center gap-2 text-[#64748b]">
              <span className={`w-2 h-2 rounded-full animate-pulse ${loading ? 'bg-amber-500' : 'bg-emerald-500'}`}></span>
              <p className="text-sm font-medium">
                {loading ? 'Synchronizing data...' : 'All systems operational • Live Data'}
              </p>
            </div>
          </motion.div>
          <div className="flex gap-4">
            <button onClick={fetchData} className="flex items-center gap-3 px-5 py-3 rounded-2xl border border-[#ffffff08] bg-[#ffffff03] hover:bg-[#ffffff08] hover:border-[#ffffff14] transition-all text-sm font-bold text-[#f8fafc]">
              <RefreshCw size={18} className={loading ? 'animate-spin' : ''} /> Refresh
            </button>
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setShowNewProjectModal(true)}
              className="flex items-center gap-3 px-6 py-3 rounded-2xl bg-gradient-premium shadow-xl shadow-indigo-600/20 text-sm font-bold text-white"
            >
              <Plus size={20} /> New Project
            </motion.button>
          </div>
        </header>

        <AnimatePresence mode="wait">
          {activeTab === 'overview' ? (
            <motion.div key="overview" initial={{ opacity: 1 }} exit={{ opacity: 0, y: -20 }} transition={{ duration: 0.2 }}>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
                <StatCard title="Total Requests" value={stats?.total_requests?.toLocaleString() || '0'} sub="Real-time activity" trend="up" icon={<Activity className="text-indigo-400" />} />
                <StatCard title="Avg Latency" value={`${stats?.avg_latency_ms || 0}ms`} sub="System performance" trend="none" icon={<RefreshCw className="text-purple-400" />} />
                <StatCard title="Most Active Model" value={stats?.top_models?.[0]?.name || 'N/A'} sub="Highest demand" trend="none" icon={<Database className="text-pink-400" />} />
                <StatCard title="Active Projects" value={projects.filter(p => p.is_active).length.toString()} sub={`${projects.length} total registered`} trend="none" icon={<Users className="text-indigo-400" />} />
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
                <div className="lg:col-span-2 glass-card rounded-[32px] p-10">
                  <h3 className="text-2xl font-bold mb-10">Traffic Activity</h3>
                  <div className="h-[350px] w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <AreaChart data={CHART_DATA}>
                        <defs>
                          <linearGradient id="colorReq" x1="0" y1="0" x2="0" y2="1"><stop offset="5%" stopColor="#6366f1" stopOpacity={0.4} /><stop offset="95%" stopColor="#6366f1" stopOpacity={0} /></linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} />
                        <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#64748b', fontSize: 12 }} />
                        <YAxis axisLine={false} tickLine={false} tick={{ fill: '#64748b', fontSize: 12 }} />
                        <Tooltip contentStyle={{ backgroundColor: 'rgba(9, 9, 11, 0.9)', backdropFilter: 'blur(10px)', border: '1px solid #ffffff14', borderRadius: '16px' }} itemStyle={{ color: '#f8fafc', fontWeight: 'bold' }} />
                        <Area type="monotone" dataKey="requests" stroke="#6366f1" strokeWidth={4} fillOpacity={1} fill="url(#colorReq)" />
                      </AreaChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                <div className="glass-card rounded-[32px] p-10">
                  <h3 className="text-2xl font-bold mb-8">Model Ranking</h3>
                  <div className="space-y-8">
                    {stats?.top_models?.map((model, i) => (
                      <div key={model.name} className="group">
                        <div className="flex justify-between items-center mb-3">
                          <p className="font-bold text-white uppercase tracking-wider text-xs">{model.name}</p>
                          <p className="text-sm font-bold text-[#94a3b8]">{model.count.toLocaleString()}</p>
                        </div>
                        <div className="relative w-full h-3 bg-[#ffffff08] rounded-full overflow-hidden">
                          <motion.div initial={{ width: 0 }} animate={{ width: `${(model.count / (stats.top_models[0].count || 1)) * 100}%` }} className="absolute top-0 left-0 h-full rounded-full bg-gradient-premium" />
                        </div>
                      </div>
                    ))}
                    {(!stats?.top_models || stats.top_models.length === 0) && <p className="text-sm text-[#64748b] text-center py-10">No traffic data available yet.</p>}
                  </div>
                </div>
              </div>
            </motion.div>
          ) : activeTab === 'projects' ? (
            <motion.div key="projects" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="glass-card rounded-[32px] p-10">
              <div className="overflow-x-auto">
                <table className="w-full text-left">
                  <thead>
                    <tr className="border-b border-[#ffffff08] text-[#64748b] text-xs font-bold uppercase tracking-widest">
                      <th className="pb-4 px-4">Project</th><th className="pb-4 px-4">API Key</th><th className="pb-4 px-4">Status</th><th className="pb-4 px-4 text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#ffffff05]">
                    {projects.map((project) => (
                      <tr key={project.id} className="group hover:bg-[#ffffff03] transition-colors">
                        <td className="py-4 px-4"><p className="font-bold text-white">{project.name}</p><p className="text-[10px] text-[#64748b]">{project.id}</p></td>
                        <td className="py-4 px-4 font-mono text-[10px] text-[#94a3b8]">{project.api_key.substring(0, 16)}...</td>
                        <td className="py-4 px-4"><span className={`px-2 py-1 rounded-lg text-[10px] font-bold ${project.is_active ? 'bg-emerald-500/10 text-emerald-400' : 'bg-red-500/10 text-red-400'}`}>{project.is_active ? 'ACTIVE' : 'INACTIVE'}</span></td>
                        <td className="py-4 px-4 text-right"><button onClick={() => handleToggleProject(project.id)} className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${project.is_active ? 'border border-red-500/20 text-red-400 hover:bg-red-500/10' : 'border border-emerald-500/20 text-emerald-400 hover:bg-emerald-500/10'}`}>{project.is_active ? 'Deactivate' : 'Activate'}</button></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </motion.div>
          ) : <div className="py-20 text-center glass-card rounded-[32px] text-[#64748b]">Under Construction</div>}
        </AnimatePresence>

        <NewProjectModal isOpen={showNewProjectModal} onClose={() => setShowNewProjectModal(false)} onCreated={fetchData} />
      </main>
    </div>
  );
}

function NewProjectModal({ isOpen, onClose, onCreated }) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [models, setModels] = useState('llama3, mistral');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const res = await fetch('/admin/projects', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Admin-Key': ADMIN_KEY },
        body: JSON.stringify({ name, description, allowed_models: models.split(',').map(m => m.trim()) })
      });
      if (res.ok) {
        setName(''); setDescription(''); setModels('llama3, mistral');
        onCreated();
        onClose();
      }
    } catch (err) { console.error(err); }
    finally { setSubmitting(false); }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-6">
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onClick={onClose} className="absolute inset-0 bg-[#000000a0] backdrop-blur-md" />
          <motion.div initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.9, opacity: 0 }} className="relative w-full max-w-lg glass-panel rounded-[32px] p-10 border border-[#ffffff10] shadow-2xl">
            <div className="flex justify-between items-center mb-8">
              <h3 className="text-2xl font-bold text-white font-display">Create New Project</h3>
              <button onClick={onClose} className="p-2 hover:bg-white/5 rounded-full text-[#64748b] hover:text-white transition-all"><X size={24} /></button>
            </div>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label className="block text-xs font-bold text-[#64748b] uppercase tracking-widest mb-2">Project Name</label>
                <input required value={name} onChange={e => setName(e.target.value)} className="w-full bg-white/5 border border-[#ffffff10] rounded-2xl px-5 py-4 text-white placeholder-[#475569] outline-none focus:border-indigo-500/50 transition-all font-bold" placeholder="e.g. Acme AI Integration" />
              </div>
              <div>
                <label className="block text-xs font-bold text-[#64748b] uppercase tracking-widest mb-2">Description</label>
                <textarea value={description} onChange={e => setDescription(e.target.value)} className="w-full bg-white/5 border border-[#ffffff10] rounded-2xl px-5 py-4 text-white placeholder-[#475569] outline-none focus:border-indigo-500/50 transition-all h-24 resize-none" placeholder="Short summary of this project..." />
              </div>
              <div>
                <label className="block text-xs font-bold text-[#64748b] uppercase tracking-widest mb-2">Allowed Models (Comma separated)</label>
                <input value={models} onChange={e => setModels(e.target.value)} className="w-full bg-white/5 border border-[#ffffff10] rounded-2xl px-5 py-4 text-white placeholder-[#475569] outline-none focus:border-indigo-500/50 transition-all font-mono text-sm" placeholder="llama3, mistral, gemma" />
                <p className="mt-2 text-[10px] text-indigo-400 font-bold tracking-wider">Models will be mapped to Ollama inventory</p>
              </div>
              <div className="pt-4 flex gap-4">
                <button type="button" onClick={onClose} className="flex-1 py-4 rounded-2xl border border-[#ffffff08] text-sm font-bold text-[#f8fafc] hover:bg-white/5 transition-all">Cancel</button>
                <button type="submit" disabled={submitting} className="flex-1 py-4 rounded-2xl bg-gradient-premium shadow-xl shadow-indigo-600/20 text-sm font-bold text-white disabled:opacity-50">
                  {submitting ? 'Creating...' : 'Create Project'}
                </button>
              </div>
            </form>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}

function NavItem({ icon, label, active, onClick, danger }) {
  return (
    <motion.button whileHover={{ x: 5 }} onClick={onClick} className={`w-full flex items-center gap-4 px-6 py-4 rounded-2xl transition-all duration-300 relative group ${active ? 'text-white' : danger ? 'text-red-400/70 hover:text-red-400' : 'text-[#64748b] hover:text-white'}`}>
      {active && <motion.div layoutId="nav-bg" className="absolute inset-0 bg-white/5 border border-white/10 rounded-2xl z-0" />}
      <span className={`z-10 transition-transform ${active ? 'scale-110 text-indigo-400' : 'group-hover:scale-110'}`}>{icon}</span>
      <span className="z-10 font-bold tracking-wide">{label}</span>
      {active && <div className="absolute right-6 w-1.5 h-1.5 bg-indigo-500 rounded-full shadow-glow" />}
    </motion.button>
  );
}

function StatCard({ title, value, sub, trend, icon }) {
  return (
    <div className="glass-card rounded-3xl p-8 group">
      <div className="flex justify-between items-start mb-6">
        <div className="p-3 bg-white/5 rounded-2xl group-hover:bg-indigo-500/10 transition-colors">{icon}</div>
        <button className="text-[#64748b] hover:text-white transition-colors"><MoreVertical size={18} /></button>
      </div>
      <div>
        <p className="text-[#94a3b8] text-sm font-bold uppercase tracking-widest mb-2">{title}</p>
        <h4 className="text-3xl font-extrabold mb-2 font-display">{value}</h4>
        <div className="flex items-center gap-2">
          {trend === 'up' && <span className="text-[10px] bg-emerald-500/10 text-emerald-400 px-2 py-0.5 rounded-full font-bold">↑ GROWING</span>}
          <p className="text-xs text-[#64748b] font-medium">{sub}</p>
        </div>
      </div>
    </div>
  );
}

export default App;

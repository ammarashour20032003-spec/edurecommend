import { useState, useEffect } from 'react';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Content from './pages/Content';
import Activity from './pages/Activity';
import Saved from './pages/Saved';
import { logout } from './services/api';

export default function App() {
  const [user, setUser]       = useState(null);
  const [page, setPage]       = useState('login');
  const [activePage, setActivePage] = useState('dashboard');

  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    const token     = localStorage.getItem('token');
    if (savedUser && token) {
      setUser(JSON.parse(savedUser));
      setPage('app');
    }
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    setPage('app');
  };

  const handleRegister = () => {
    setPage('login');
  };

  const handleLogout = async () => {
    try { await logout(); } catch (e) {}
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    setPage('login');
  };

  if (page === 'login') {
    return (
      <div>
        <Login onLogin={handleLogin} />
        <div className="text-center mt-4 pb-8">
          <span className="text-gray-500 text-sm">Don't have an account? </span>
          <button
            onClick={() => setPage('register')}
            className="text-indigo-600 text-sm font-medium hover:underline"
          >
            Register
          </button>
        </div>
      </div>
    );
  }

  if (page === 'register') {
    return (
      <div>
        <Register onRegister={handleRegister} />
        <div className="text-center mt-4 pb-8">
          <span className="text-gray-500 text-sm">Already have an account? </span>
          <button
            onClick={() => setPage('login')}
            className="text-indigo-600 text-sm font-medium hover:underline"
          >
            Sign In
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navbar */}
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <h1 className="text-xl font-bold text-indigo-700">EduRecommend</h1>
          <div className="flex items-center gap-6">
            <button
              onClick={() => setActivePage('dashboard')}
              className={`text-sm font-medium transition ${activePage === 'dashboard' ? 'text-indigo-600' : 'text-gray-500 hover:text-gray-800'}`}
            >
              Recommendations
            </button>
            <button
              onClick={() => setActivePage('content')}
              className={`text-sm font-medium transition ${activePage === 'content' ? 'text-indigo-600' : 'text-gray-500 hover:text-gray-800'}`}
            >
              Browse
            </button>
<button
  onClick={() => setActivePage('activity')}
  className={`text-sm font-medium transition ${activePage === 'activity' ? 'text-indigo-600' : 'text-gray-500 hover:text-gray-800'}`}
>
  My Activity
</button>
<button
  onClick={() => setActivePage('saved')}
  className={`text-sm font-medium transition ${activePage === 'saved' ? 'text-indigo-600' : 'text-gray-500 hover:text-gray-800'}`}
>
  Saved
</button>
            <div className="flex items-center gap-3">
              <span className="text-sm text-gray-600">{user?.full_name}</span>
              <button
                onClick={handleLogout}
                className="text-sm text-red-500 hover:text-red-700 transition"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Pages */}
      <main className="py-6">
        {activePage === 'dashboard' && <Dashboard user={user} />}
        {activePage === 'content'   && <Content />}
	{activePage === 'activity'  && <Activity />}
	{activePage === 'saved' && <Saved />}
      </main>
    </div>
  );
}
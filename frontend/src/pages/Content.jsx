import { useState, useEffect } from 'react';
import { getContent, searchContent, logInteraction, saveContent } from '../services/api';

export default function Content() {
  const [contents, setContents]     = useState([]);
  const [search, setSearch]         = useState('');
  const [filter, setFilter]         = useState({ field: '', level: '', type: '' });
  const [loading, setLoading]       = useState(true);
  const [message, setMessage]       = useState('');
  const [savedItems, setSavedItems] = useState({});

  useEffect(() => {
    fetchContent();
  }, [filter]);

  const fetchContent = async () => {
    setLoading(true);
    try {
      const res = await getContent(filter);
      setContents(res.data.content);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!search.trim()) return fetchContent();
    setLoading(true);
    try {
      const res = await searchContent(search);
      setContents(res.data.results);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleInteraction = async (contentId, action, url) => {
    try {
      await logInteraction({ content_id: contentId, action, duration_seconds: 0 });
      setMessage(`Logged as ${action}!`);
      setTimeout(() => setMessage(''), 2000);
      if (url) window.open(url, '_blank');
    } catch (err) {
      console.error(err);
    }
  };

  const handleSave = async (contentId) => {
    try {
      const res = await saveContent(contentId);
      setSavedItems(prev => ({ ...prev, [contentId]: res.data.saved }));
      setMessage(res.data.saved ? 'Saved!' : 'Unsaved!');
      setTimeout(() => setMessage(''), 2000);
    } catch (err) {
      console.error(err);
    }
  };

  const getTypeIcon = (type) => {
    if (type === 'video')  return '🎥';
    if (type === 'course') return '📚';
    return '📄';
  };

  const getFieldColor = (field) => {
    const colors = {
      'Cybersecurity':    'bg-red-100 text-red-700',
      'Machine Learning': 'bg-purple-100 text-purple-700',
      'Data Science':     'bg-blue-100 text-blue-700',
      'Web Development':  'bg-green-100 text-green-700',
      'Linux':            'bg-yellow-100 text-yellow-700',
      'Cloud':            'bg-sky-100 text-sky-700',
    };
    return colors[field] || 'bg-gray-100 text-gray-700';
  };

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Browse Content</h2>

      {message && (
        <div className="bg-green-50 text-green-700 px-4 py-3 rounded-lg mb-4 text-sm">
          {message}
        </div>
      )}

      {/* Search */}
      <form onSubmit={handleSearch} className="flex gap-2 mb-4">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search by title..."
          className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-400"
        />
        <button
          type="submit"
          className="bg-indigo-600 text-white px-5 py-2 rounded-lg font-semibold hover:bg-indigo-700 transition"
        >
          Search
        </button>
      </form>

      {/* Filters */}
      <div className="flex gap-3 mb-6 flex-wrap">
        <select
          value={filter.field}
          onChange={(e) => setFilter({ ...filter, field: e.target.value })}
          className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
        >
          <option value="">All Fields</option>
          <option value="Cybersecurity">Cybersecurity</option>
          <option value="Machine Learning">Machine Learning</option>
          <option value="Data Science">Data Science</option>
          <option value="Web Development">Web Development</option>
          <option value="Linux">Linux</option>
          <option value="Cloud">Cloud</option>
        </select>

        <select
          value={filter.level}
          onChange={(e) => setFilter({ ...filter, level: e.target.value })}
          className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
        >
          <option value="">All Levels</option>
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </select>

        <select
          value={filter.type}
          onChange={(e) => setFilter({ ...filter, type: e.target.value })}
          className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
        >
          <option value="">All Types</option>
          <option value="video">Video</option>
          <option value="course">Course</option>
          <option value="article">Article</option>
        </select>

        <button
          onClick={() => { setFilter({ field: '', level: '', type: '' }); setSearch(''); }}
          className="text-sm text-indigo-600 hover:underline"
        >
          Clear filters
        </button>
      </div>

      {/* Content Grid */}
      {loading ? (
        <div className="text-center text-gray-400 py-20">Loading content...</div>
      ) : contents.length === 0 ? (
        <div className="text-center text-gray-400 py-20">No content found</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {contents.map((c) => (
            <div key={c.id} className="bg-white rounded-xl shadow-sm border p-5 hover:shadow-md transition">
              <div className="flex items-start justify-between mb-3">
                <span className="text-2xl">{getTypeIcon(c.type)}</span>
                <span className={`text-xs px-2 py-1 rounded-full font-medium ${getFieldColor(c.field)}`}>
                  {c.field}
                </span>
              </div>

              <h3 className="font-semibold text-gray-800 mb-1">{c.title}</h3>
              <div className="flex items-center gap-3 text-xs text-gray-400 mb-4">
                <span className="capitalize">{c.level}</span>
                <span>·</span>
                <span className="capitalize">{c.type}</span>
                {c.avg_rating > 0 && (
                  <>
                    <span>·</span>
                    <span>⭐ {c.avg_rating}</span>
                  </>
                )}
              </div>

              <div className="flex gap-2">
                <button
                  onClick={() => handleInteraction(c.id, 'viewed', c.url)}
                  className="flex-1 bg-indigo-50 text-indigo-700 py-2 rounded-lg text-sm font-medium hover:bg-indigo-100 transition"
                >
                  Open →
                </button>
                <button
                  onClick={() => handleInteraction(c.id, 'liked', null)}
                  className="bg-pink-50 text-pink-600 px-3 py-2 rounded-lg text-sm hover:bg-pink-100 transition"
                >
                  ♥
                </button>
                <button
                  onClick={() => handleSave(c.id)}
                  className={`px-3 py-2 rounded-lg text-sm transition ${
                    savedItems[c.id]
                      ? 'bg-yellow-100 text-yellow-700 hover:bg-yellow-200'
                      : 'bg-yellow-50 text-yellow-600 hover:bg-yellow-100'
                  }`}
                >
                  🔖
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
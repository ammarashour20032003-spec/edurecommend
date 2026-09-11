import { useState, useEffect } from 'react';
import { getUserInteractions, getContentById } from '../services/api';

export default function Activity() {
  const [interactions, setInteractions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchInteractions();
  }, []);

  const fetchInteractions = async () => {
    try {
      const res = await getUserInteractions();
      const filtered = res.data.interactions.filter(i => i.action !== 'rated');

      const withContent = await Promise.all(
        filtered.map(async (i) => {
          try {
            const c = await getContentById(i.content_id);
            return { ...i, contentTitle: c.data.content.title };
          } catch {
            return { ...i, contentTitle: i.content_id };
          }
        })
      );

      setInteractions(withContent);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getActionColor = (action) => {
    const colors = {
      'viewed':     'bg-blue-100 text-blue-700',
      'liked':      'bg-pink-100 text-pink-700',
      'bookmarked': 'bg-yellow-100 text-yellow-700',
    };
    return colors[action] || 'bg-gray-100 text-gray-700';
  };

  const getActionIcon = (action) => {
    if (action === 'viewed')     return '👁️';
    if (action === 'liked')      return '♥';
    if (action === 'bookmarked') return '🔖';
    return '•';
  };

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">My Activity</h2>
      {loading ? (
        <div className="text-center text-gray-400 py-20">Loading activity...</div>
      ) : interactions.length === 0 ? (
        <div className="text-center text-gray-400 py-20">No activity yet — start browsing content!</div>
      ) : (
        <div className="space-y-3">
          {interactions.slice().reverse().map((i) => (
            <div key={i.id} className="bg-white rounded-xl border shadow-sm px-5 py-4 flex items-center justify-between">
              <div className="flex items-center gap-4">
                <span className="text-xl">{getActionIcon(i.action)}</span>
                <div>
                  <p className="text-sm font-medium text-gray-800">{i.contentTitle}</p>
                  <p className="text-xs text-gray-400">{new Date(i.interacted_at).toLocaleString()}</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                {i.duration_seconds > 0 && (
                  <span className="text-xs text-gray-500">{i.duration_seconds}s</span>
                )}
                <span className={`text-xs px-2 py-1 rounded-full font-medium ${getActionColor(i.action)}`}>
                  {i.action}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
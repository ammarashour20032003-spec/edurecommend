import { useState, useEffect } from 'react';
import { getSaved } from '../services/api';

export default function Saved() {
  const [saved, setSaved]     = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSaved();
  }, []);

  const fetchSaved = async () => {
    try {
      const res = await getSaved();
      setSaved(res.data.saved);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
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
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Saved Resources</h2>

      {loading ? (
        <div className="text-center text-gray-400 py-20">Loading saved items...</div>
      ) : saved.length === 0 ? (
        <div className="text-center py-20">
          <p className="text-gray-400 text-lg mb-2">No saved resources yet</p>
          <p className="text-gray-400 text-sm">Click 🔖 on any resource to save it here</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {saved.map((item) => (
            <div key={item.recommendation_id} className="bg-white rounded-xl shadow-sm border p-5 hover:shadow-md transition">
              <div className="flex items-start justify-between mb-3">
                <span className="text-2xl">{getTypeIcon(item.content?.type)}</span>
                <span className={`text-xs px-2 py-1 rounded-full font-medium ${getFieldColor(item.content?.field)}`}>
                  {item.content?.field}
                </span>
              </div>

              <h3 className="font-semibold text-gray-800 mb-1">{item.content?.title}</h3>
              <div className="flex items-center gap-3 text-xs text-gray-400 mb-4">
                <span className="capitalize">{item.content?.level}</span>
                <span>·</span>
                <span className="capitalize">{item.content?.type}</span>
              </div>

              <button
                onClick={() => window.open(item.content?.url, '_blank')}
                className="w-full bg-indigo-50 text-indigo-700 py-2 rounded-lg text-sm font-medium hover:bg-indigo-100 transition"
              >
                Open Resource →
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
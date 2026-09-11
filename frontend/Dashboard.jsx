import { useState, useEffect } from 'react';
import { getRecommendations, generateRecommendations, markClicked, saveRecommendation } from '../services/api';

export default function Dashboard({ user }) {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const fetchRecommendations = async () => {
    try {
      const res = await getRecommendations();
      setRecommendations(res.data.recommendations);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async () => {
    setGenerating(true);
    setMessage('');
    try {
      const res = await generateRecommendations();
      setMessage(res.data.message);
      await fetchRecommendations();
    } catch (err) {
      setMessage('Failed to generate recommendations');
    } finally {
      setGenerating(false);
    }
  };

  const handleClick = async (rec) => {
    try {
      await markClicked(rec.recommendation_id);
      window.open(rec.content.url, '_blank');
      setRecommendations(prev =>
        prev.map(r =>
          r.recommendation_id === rec.recommendation_id
            ? { ...r, clicked: true }
            : r
        )
      );
    } catch (err) {
      console.error(err);
    }
  };

  const handleSave = async (rec) => {
    try {
      const res = await saveRecommendation(rec.recommendation_id);
      setRecommendations(prev =>
        prev.map(r =>
          r.recommendation_id === rec.recommendation_id
            ? { ...r, saved: res.data.saved }
            : r
        )
      );
    } catch (err) {
      console.error(err);
    }
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

  const getTypeIcon = (type) => {
    if (type === 'video') return '🎥';
    if (type === 'course') return '📚';
    return '📄';
  };

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">Your Recommendations</h2>
          <p className="text-gray-500 mt-1">
            Personalized for {user.full_name} · {user.specialization}
          </p>
        </div>
        <button
          onClick={handleGenerate}
          disabled={generating}
          className="bg-indigo-600 text-white px-5 py-2 rounded-lg font-semibold hover:bg-indigo-700 transition disabled:opacity-50"
        >
          {generating ? 'Generating...' : 'Generate New'}
        </button>
      </div>

      {message && (
        <div className="bg-green-50 text-green-700 px-4 py-3 rounded-lg mb-6 text-sm">
          {message}
        </div>
      )}

      {loading ? (
        <div className="text-center text-gray-400 py-20">Loading recommendations...</div>
      ) : recommendations.length === 0 ? (
        <div className="text-center py-20">
          <p className="text-gray-400 text-lg mb-4">No recommendations yet</p>
          <button
            onClick={handleGenerate}
            className="bg-indigo-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-indigo-700 transition"
          >
            Generate Recommendations
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {recommendations.map((rec) => (
            <div
              key={rec.recommendation_id}
              className={rec.clicked ? 'bg-white rounded-xl shadow-sm border p-5 hover:shadow-md transition opacity-70' : 'bg-white rounded-xl shadow-sm border p-5 hover:shadow-md transition'}
            >
              <div className="flex items-start justify-between mb-3">
                <span className="text-2xl">{getTypeIcon(rec.content?.type)}</span>
                <div className="flex items-center gap-2">
                  <span className={getFieldColor(rec.content?.field) + ' text-xs px-2 py-1 rounded-full font-medium'}>
                    {rec.content?.field}
                  </span>
                  {rec.clicked && (
                    <span className="text-xs px-2 py-1 rounded-full bg-gray-100 text-gray-500">
                      Visited
                    </span>
                  )}
                </div>
              </div>

              <h3 className="font-semibold text-gray-800 mb-1">{rec.content?.title}</h3>

              <div className="flex items-center gap-3 text-xs text-gray-400 mb-4">
                <span className="capitalize">{rec.content?.level}</span>
                <span>·</span>
                <span className="capitalize">{rec.content?.type}</span>
                <span>·</span>
                <span>Score: {rec.score}</span>
              </div>

              <div className="flex gap-2">
                <button
                  onClick={() => handleClick(rec)}
                  className="flex-1 bg-indigo-50 text-indigo-700 py-2 rounded-lg text-sm font-medium hover:bg-indigo-100 transition"
                >
                  Open Resource
                </button>
                <button
                  onClick={() => handleSave(rec)}
                  className={rec.saved ? 'px-4 py-2 rounded-lg text-sm font-medium transition bg-yellow-100 text-yellow-700 hover:bg-yellow-200' : 'px-4 py-2 rounded-lg text-sm font-medium transition bg-gray-100 text-gray-500 hover:bg-gray-200'}
                >
                  {rec.saved ? 'Saved' : 'Save'}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

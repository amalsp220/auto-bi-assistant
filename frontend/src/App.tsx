import { useState } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, ScatterChart, Scatter, PieChart, Pie, Cell } from 'recharts';

const API_BASE = import.meta.env.VITE_API_URL || '';

const COLORS = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6'];

function App() {
  const [sessionId, setSessionId] = useState('');
  const [filename, setFilename] = useState('');
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [question, setQuestion] = useState('');
  const [result, setResult] = useState<any>(null);
  const [chartSpec, setChartSpec] = useState<any>(null);
  const [narrative, setNarrative] = useState('');
  const [report, setReport] = useState('');
  const [uploading, setUploading] = useState(false);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await axios.post(`${API_BASE}/api/upload`, formData);
      setSessionId(res.data.session_id);
      setFilename(res.data.filename);
      setProfile(res.data.profile);
      console.log('Upload result:', res.data);
    } catch (err) {
      alert('Upload failed: ' + (err as any).message);
    } finally {
      setUploading(false);
    }
  };

  const handleAsk = async () => {
    if (!sessionId || !question) return;
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/api/ask`, { session_id: sessionId, question });
      console.log('Ask result:', res.data);
      setResult(res.data.result);
      setChartSpec(res.data.chart_spec);
      setNarrative(res.data.narrative);
    } catch (err) {
      alert('Query failed: ' + (err as any).message);
    } finally {
      setLoading(false);
    }
  };

  const handleReport = async () => {
    if (!sessionId || !question) return;
    try {
      const res = await axios.post(`${API_BASE}/api/report`, { session_id: sessionId, question });
      setReport(res.data.report);
    } catch (err) {
      alert('Report failed: ' + (err as any).message);
    }
  };

  const renderChart = () => {
    if (!chartSpec) return null;
    const { type, x_key, y_key, data } = chartSpec;
    if (type === 'bar' || type === 'histogram') {
      return (
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={x_key} tick={{fontSize: 10}} />
            <YAxis />
            <Tooltip />
            <Bar dataKey={y_key} fill="#3b82f6" />
          </BarChart>
        </ResponsiveContainer>
      );
    }
    if (type === 'line') {
      return (
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={x_key} tick={{fontSize: 10}} />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey={y_key} stroke="#3b82f6" />
          </LineChart>
        </ResponsiveContainer>
      );
    }
    if (type === 'scatter') {
      return (
        <ResponsiveContainer width="100%" height={300}>
          <ScatterChart>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={x_key} type="number" />
            <YAxis dataKey={y_key} type="number" />
            <Tooltip />
            <Scatter data={data} fill="#3b82f6" />
          </ScatterChart>
        </ResponsiveContainer>
      );
    }
    if (type === 'pie') {
      return (
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie data={data} dataKey={y_key} nameKey={x_key} cx="50%" cy="50%" outerRadius={80}>
              {data.map((_: any, i: number) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      );
    }
    return null;
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Auto-BI Assistant</h1>
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Upload CSV Dataset</h2>
        <input type="file" accept=".csv" onChange={handleUpload} disabled={uploading} className="block" />
        {uploading && <p className="text-blue-600 mt-2">Uploading...</p>}
        {filename && <p className="text-green-600 mt-2">Loaded: {filename}</p>}
      </div>
      {profile && (
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Dataset Profile</h2>
          <p><strong>Rows:</strong> {profile.shape.rows} | <strong>Columns:</strong> {profile.shape.columns}</p>
          <div className="mt-4 max-h-40 overflow-auto text-sm">
            <pre>{JSON.stringify(profile.columns, null, 2)}</pre>
          </div>
        </div>
      )}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Ask a Question</h2>
        <input
          type="text"
          placeholder="e.g., What is the correlation between X and Y?"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="w-full border rounded px-4 py-2 mb-3"
        />
        <div className="flex gap-3">
          <button onClick={handleAsk} disabled={loading || !sessionId} className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50">
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>
          <button onClick={handleReport} disabled={!sessionId} className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50">
            Generate Report
          </button>
        </div>
      </div>
      {result && (
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Results</h2>
          {narrative && <p className="mb-4">{narrative}</p>}
          {chartSpec && (
            <div className="mb-4">
              <h3 className="font-medium mb-2">Chart: {chartSpec.label}</h3>
              {renderChart()}
            </div>
          )}
          {result.data && (
            <div>
              <h3 className="font-medium mb-2">Data</h3>
              <pre className="text-sm bg-gray-100 p-3 rounded max-h-40 overflow-auto">{JSON.stringify(result.data, null, 2)}</pre>
            </div>
          )}
          {result.code_executed && (
            <div className="mt-4">
              <h3 className="font-medium mb-2">Generated Code</h3>
              <pre className="text-sm bg-gray-100 p-3 rounded max-h-40 overflow-auto">{result.code_executed}</pre>
            </div>
          )}
        </div>
      )}
      {report && (
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Report</h2>
          <a href={`data:text/markdown;charset=utf-8,${encodeURIComponent(report)}`} download="report.md" className="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 inline-block mb-4">Download Markdown Report</a>
          <pre className="text-sm bg-gray-100 p-3 rounded max-h-64 overflow-auto whitespace-pre-wrap">{report}</pre>
        </div>
      )}
    </div>
  );
}

export default App;

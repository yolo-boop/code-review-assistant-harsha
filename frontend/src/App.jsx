import { useState, useEffect } from 'react';
import axios from 'axios';
import { Upload, FileCode, CheckCircle, AlertCircle, TrendingUp, Shield, Zap, Code } from 'lucide-react';
import './App.css';

const API_URL = 'http://localhost:5000/api';

function App() {
  const [code, setCode] = useState('');
  const [filename, setFilename] = useState('');
  const [language, setLanguage] = useState('javascript');
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [activeTab, setActiveTab] = useState('review');

  useEffect(() => {
    if (activeTab === 'history') {
      fetchReviews();
    }
  }, [activeTab]);

  const fetchReviews = async () => {
    try {
      const response = await axios.get(`${API_URL}/reviews`);
      setReviews(response.data.reviews);
    } catch (error) {
      console.error('Error fetching reviews:', error);
    }
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setFilename(file.name);
      const reader = new FileReader();
      reader.onload = (e) => {
        setCode(e.target.result);
      };
      reader.readAsText(file);

      // Detect language from extension
      const ext = file.name.split('.').pop().toLowerCase();
      const langMap = {
        'js': 'javascript',
        'jsx': 'javascript',
        'ts': 'typescript',
        'tsx': 'typescript',
        'py': 'python',
        'java': 'java',
        'cpp': 'cpp',
        'c': 'c',
        'go': 'go',
        'rs': 'rust',
        'rb': 'ruby',
        'php': 'php',
        'cs': 'csharp',
        'swift': 'swift',
        'kt': 'kotlin'
      };
      setLanguage(langMap[ext] || 'text');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!code.trim()) {
      alert('Please enter or upload some code');
      return;
    }

    setLoading(true);
    setAnalysis(null);

    try {
      const response = await axios.post(`${API_URL}/review`, {
        code,
        filename: filename || 'untitled.txt',
        language
      });

      setAnalysis(response.data.analysis);
    } catch (error) {
      alert('Error analyzing code: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 8) return '#10b981';
    if (score >= 6) return '#f59e0b';
    return '#ef4444';
  };

  const getSeverityColor = (severity) => {
    const colors = {
      high: '#ef4444',
      medium: '#f59e0b',
      low: '#10b981'
    };
    return colors[severity?.toLowerCase()] || '#6b7280';
  };

  return (
    <div className="App">
      <header className="header">
        <div className="header-content">
          <FileCode size={32} />
          <h1>Code Review Assistant</h1>
          <p>AI-powered code analysis and review</p>
        </div>
      </header>

      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'review' ? 'active' : ''}`}
          onClick={() => setActiveTab('review')}
        >
          <Code size={20} />
          New Review
        </button>
        <button 
          className={`tab ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => setActiveTab('history')}
        >
          <FileCode size={20} />
          Review History
        </button>
      </div>

      <main className="main-content">
        {activeTab === 'review' ? (
          <div className="review-section">
            <form onSubmit={handleSubmit} className="upload-form">
              <div className="form-group">
                <label>Upload Code File</label>
                <div className="file-upload">
                  <input
                    type="file"
                    onChange={handleFileUpload}
                    accept=".js,.jsx,.ts,.tsx,.py,.java,.cpp,.c,.go,.rs,.rb,.php,.cs,.swift,.kt"
                    id="file-input"
                  />
                  <label htmlFor="file-input" className="file-label">
                    <Upload size={20} />
                    {filename || 'Choose a file'}
                  </label>
                </div>
              </div>

              <div className="form-group">
                <label>Or Paste Your Code</label>
                <textarea
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  placeholder="Paste your code here..."
                  rows={15}
                  className="code-input"
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label>Filename</label>
                  <input
                    type="text"
                    value={filename}
                    onChange={(e) => setFilename(e.target.value)}
                    placeholder="example.js"
                    className="text-input"
                  />
                </div>

                <div className="form-group">
                  <label>Language</label>
                  <select 
                    value={language} 
                    onChange={(e) => setLanguage(e.target.value)}
                    className="select-input"
                  >
                    <option value="javascript">JavaScript</option>
                    <option value="typescript">TypeScript</option>
                    <option value="python">Python</option>
                    <option value="java">Java</option>
                    <option value="cpp">C++</option>
                    <option value="go">Go</option>
                    <option value="rust">Rust</option>
                    <option value="ruby">Ruby</option>
                    <option value="php">PHP</option>
                  </select>
                </div>
              </div>

              <button type="submit" disabled={loading} className="submit-btn">
                {loading ? 'Analyzing...' : 'Review Code'}
              </button>
            </form>

            {loading && (
              <div className="loading">
                <div className="spinner"></div>
                <p>Analyzing your code with AI...</p>
              </div>
            )}

            {analysis && (
              <div className="analysis-results">
                <h2>Analysis Results</h2>
                
                <div className="score-card">
                  <h3>Overall Score</h3>
                  <div className="score-circle" style={{ borderColor: getScoreColor(analysis.overallScore) }}>
                    <span className="score-number">{analysis.overallScore}</span>
                    <span className="score-max">/10</span>
                  </div>
                  <p className="summary">{analysis.summary}</p>
                </div>

                <div className="metrics-grid">
                  <div className="metric-card">
                    <div className="metric-header">
                      <Code size={24} style={{ color: '#3b82f6' }} />
                      <h4>Readability</h4>
                    </div>
                    <div className="metric-score" style={{ color: getScoreColor(analysis.readability?.score) }}>
                      {analysis.readability?.score}/10
                    </div>
                    <p>{analysis.readability?.comments}</p>
                    {analysis.readability?.issues?.length > 0 && (
                      <ul className="issue-list">
                        {analysis.readability.issues.map((issue, i) => (
                          <li key={i}>{issue}</li>
                        ))}
                      </ul>
                    )}
                  </div>

                  <div className="metric-card">
                    <div className="metric-header">
                      <CheckCircle size={24} style={{ color: '#10b981' }} />
                      <h4>Best Practices</h4>
                    </div>
                    <div className="metric-score" style={{ color: getScoreColor(analysis.bestPractices?.score) }}>
                      {analysis.bestPractices?.score}/10
                    </div>
                    <p>{analysis.bestPractices?.comments}</p>
                    {analysis.bestPractices?.violations?.length > 0 && (
                      <ul className="issue-list">
                        {analysis.bestPractices.violations.map((violation, i) => (
                          <li key={i}>{violation}</li>
                        ))}
                      </ul>
                    )}
                  </div>

                  <div className="metric-card">
                    <div className="metric-header">
                      <Shield size={24} style={{ color: '#8b5cf6' }} />
                      <h4>Security</h4>
                    </div>
                    <div className="metric-score" style={{ color: getScoreColor(analysis.security?.score) }}>
                      {analysis.security?.score}/10
                    </div>
                    {analysis.security?.issues?.map((issue, i) => (
                      <div key={i} className="security-issue">
                        <span 
                          className="severity-badge" 
                          style={{ backgroundColor: getSeverityColor(issue.severity) }}
                        >
                          {issue.severity}
                        </span>
                        <p><strong>{issue.description}</strong></p>
                        <p className="recommendation">{issue.recommendation}</p>
                      </div>
                    ))}
                  </div>

                  <div className="metric-card">
                    <div className="metric-header">
                      <Zap size={24} style={{ color: '#f59e0b' }} />
                      <h4>Performance</h4>
                    </div>
                    <div className="metric-score" style={{ color: getScoreColor(analysis.performance?.score) }}>
                      {analysis.performance?.score}/10
                    </div>
                    {analysis.performance?.suggestions?.length > 0 && (
                      <ul className="issue-list">
                        {analysis.performance.suggestions.map((suggestion, i) => (
                          <li key={i}>{suggestion}</li>
                        ))}
                      </ul>
                    )}
                  </div>
                </div>

                {analysis.bugs?.found?.length > 0 && (
                  <div className="bugs-section">
                    <h3>
                      <AlertCircle size={24} />
                      Potential Bugs
                    </h3>
                    {analysis.bugs.found.map((bug, i) => (
                      <div key={i} className="bug-card">
                        <div className="bug-header">
                          <span className="line-number">Line {bug.line}</span>
                        </div>
                        <p className="bug-description">{bug.description}</p>
                        <div className="bug-suggestion">
                          <strong>Suggestion:</strong> {bug.suggestion}
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {analysis.improvements?.length > 0 && (
                  <div className="improvements-section">
                    <h3>
                      <TrendingUp size={24} />
                      Suggested Improvements
                    </h3>
                    {analysis.improvements.map((improvement, i) => (
                      <div key={i} className="improvement-card">
                        <div className="improvement-header">
                          <span className="category">{improvement.category}</span>
                          <span 
                            className="impact-badge"
                            style={{ backgroundColor: getSeverityColor(improvement.impact) }}
                          >
                            {improvement.impact} impact
                          </span>
                        </div>
                        <p>{improvement.description}</p>
                        {improvement.before && improvement.after && (
                          <div className="code-comparison">
                            <div className="code-block">
                              <div className="code-label">Before:</div>
                              <pre>{improvement.before}</pre>
                            </div>
                            <div className="code-block">
                              <div className="code-label">After:</div>
                              <pre>{improvement.after}</pre>
                            </div>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        ) : (
          <div className="history-section">
            <h2>Review History</h2>
            {reviews.length === 0 ? (
              <div className="empty-state">
                <FileCode size={48} />
                <p>No reviews yet. Start by reviewing some code!</p>
              </div>
            ) : (
              <div className="reviews-list">
                {reviews.map((review) => (
                  <div key={review.id} className="review-item">
                    <div className="review-header">
                      <h3>{review.filename}</h3>
                      <span className="review-score" style={{ color: getScoreColor(review.analysis.overallScore) }}>
                        {review.analysis.overallScore}/10
                      </span>
                    </div>
                    <div className="review-meta">
                      <span>{review.language}</span>
                      <span>{new Date(review.timestamp).toLocaleString()}</span>
                      <span>{review.codeLength} characters</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
import { useState, useEffect } from 'react';
import './App.css';

interface BlogResponse {
  content: string;
  status: string;
}

function App() {
  const [topic, setTopic] = useState('');
  const [tone, setTone] = useState('formal');
  const [blog, setBlog] = useState('');
  const [apiProvider, setApiProvider] = useState('groq');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);

  const tones = ['formal', 'casual', 'professional', 'friendly', 'technical'];
  const providers = [
    { value: 'groq', label: 'Groq' },
    { value: 'huggingface', label: 'Hugging Face' }
  ];

  // Reset copied status after 2 seconds
  useEffect(() => {
    if (copied) {
      const timer = setTimeout(() => {
        setCopied(false);
      }, 2000);
      return () => clearTimeout(timer);
    }
  }, [copied]);

  const generateBlog = async () => {
    if (!topic.trim()) {
      setError('Please enter a topic for your blog post');
      return;
    }

    setLoading(true);
    setError('');
    setBlog('');
    
    const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:3000';
    
    try {
      const response = await fetch(`${backendUrl}/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ topic, tone, apiProvider }),
      });
      
      const data: BlogResponse = await response.json();
      
      if (response.ok) {
        setBlog(data.content);
      } else {
        setError(data.status || 'Failed to generate blog. Please try again.');
      }
    } catch (err) {
      setError('Network error. Please check your connection and try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(blog);
    setCopied(true);
  };

  const formatDate = () => {
    const date = new Date();
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  const renderContent = () => {
    if (loading) {
      return (
        <div className="loader">
          <div className="loader-spinner"></div>
        </div>
      );
    }
    
    if (blog) {
      return (
        <div className="blog-content fade-in">
          <div className="blog-header">
            <h2>{topic}</h2>
            <div className="blog-meta">
              <span>{formatDate()}</span>
              <span>• {tone.charAt(0).toUpperCase() + tone.slice(1)} tone</span>
            </div>
          </div>
          <div 
            className="blog-text" 
            dangerouslySetInnerHTML={{ __html: blog.replace(/\n/g, '<br />') }} 
          />
          <div className="actions">
            <button
              onClick={copyToClipboard}
              className="btn btn-secondary"
            >
              {copied ? 'Copied!' : 'Copy to Clipboard'}
            </button>
          </div>
        </div>
      );
    }
    
    return null;
  };

  return (
    <div className="container">
      <h1>AI Blog Generator</h1>
      
      <div className="card">
        <div className="input-section">
          <div className="form-group">
            <label htmlFor="topic">Blog Topic</label>
            <input
              id="topic"
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="Enter a topic (e.g., 'Sustainable Gardening')"
            />
          </div>
          
          <div className="form-group">
            <label>Select Tone</label>
            <div className="tone-options">
              {tones.map((t) => (
                <div 
                  key={t}
                  className={`tone-option ${tone === t ? 'active' : ''}`}
                  onClick={() => setTone(t)}
                >
                  {t.charAt(0).toUpperCase() + t.slice(1)}
                </div>
              ))}
            </div>
          </div>
          <div className="form-group">
            <label>Select AI Provider</label>
            <div className="tone-options">
              {providers.map((provider) => (
                <div 
                  key={provider.value}
                  className={`tone-option ${apiProvider === provider.value ? 'active' : ''}`}
                  onClick={() => setApiProvider(provider.value)}
                >
                  {provider.label}
                </div>
              ))}
            </div>
          </div>
          <button 
            onClick={generateBlog} 
            disabled={loading}
            className="btn btn-primary"
          >
            {loading ? 'Generating...' : 'Generate Blog'}
          </button>
        </div>
      </div>
      
      {error && <div className="error fade-in">{error}</div>}
      
      {renderContent()}
    </div>
  );
}

export default App;
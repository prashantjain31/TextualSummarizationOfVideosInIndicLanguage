import React, { useState } from 'react';
import axios from 'axios';
import './App.css'

function App() {
  const [url, setUrl] = useState('');
  const [language, setLanguage] = useState('hi');
  const [translatedSummary, setTranslatedSummary] = useState('');
  const [audioUrl, setAudioUrl] = useState('');

  const handleUrlChange = (e) => {
    setUrl(e.target.value);
  };

  const handleLanguageChange = (e) => {
    setLanguage(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/process_youtube', {
        youtube_url: url,
        target_language: language
      });
      const { translated_summary, audio_file } = response.data;
      setTranslatedSummary(translated_summary);
      setAudioUrl(`data:audio/wav;base64,${audio_file}`);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="App">
      <h1>YouTube Translator</h1>
      <form onSubmit={handleSubmit}>
        <label>
          YouTube URL:
          <input type="text" value={url} onChange={handleUrlChange} required />
        </label>
        <label>
          Select Language:
          <select value={language} onChange={handleLanguageChange}>
            <option value="hi">Hindi</option>
            <option value="mr">Marathi</option>
            <option value="bn">Bangla</option>
            <option value="ta">Tamil</option>
            <option value="te">Telugu</option>
            <option value="ml">Malayalam</option>
            <option value="kn">Kannada</option>
          </select>
        </label>
        <button type="submit">Translate</button>
      </form>
      {translatedSummary && (
        <div>
          <h2>Translated Summary:</h2>
          <p>{translatedSummary}</p>
        </div>
      )}
      {audioUrl && (
        <div>
          <h2>Audio:</h2>
          <audio controls>
            <source src={audioUrl} type="audio/wav" />
            Your browser does not support the audio element.
          </audio>
        </div>
      )}
    </div>
  );
}

export default App;

import { useState } from 'react';
import Header from './components/Header';
import ImageUploader from './components/ImageUploader';
import ImageGrid from './components/ImageGrid';
import SettingsPanel from './components/SettingsPanel';
import RunButton from './components/RunButton';
import ResultsPanel from './components/ResultsPanel';
import { runAnalysis, clearFaces, resetAll } from './api';

const DEFAULT_PARAMS = {
  model_name: 'VGG-Face',
  detector_backend: 'opencv',
  distance_threshold: 0.55,
  min_confidence: 0.5,
};

export default function App() {
  const [images, setImages] = useState([]);
  const [persons, setPersons] = useState([]);
  const [loading, setLoading] = useState(false);
  const [params, setParams] = useState(DEFAULT_PARAMS);

  const handleUpload = (newImages) => {
    setImages((prev) => [...prev, ...newImages]);
  };

  const handleRun = async () => {
    setLoading(true);
    try {
      const data = await runAnalysis(params);
      setPersons(data.persons);
    } catch (e) {
      console.error('Analysis error:', e);
    } finally {
      setLoading(false);
    }
  };

  const handleClearFaces = async () => {
    try {
      await clearFaces();
      setPersons([]);
    } catch (e) {
      console.error('Clear faces error:', e);
    }
  };

  const handleReset = async () => {
    try {
      await resetAll();
      setImages([]);
      setPersons([]);
    } catch (e) {
      console.error('Reset error:', e);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header onReset={handleReset} onClearFaces={handleClearFaces} />
      <main className="max-w-6xl mx-auto p-4 sm:p-6 space-y-6">
        <ImageUploader onUpload={handleUpload} />
        <ImageGrid images={images} />
        <SettingsPanel params={params} onChange={setParams} />
        <RunButton
          onRun={handleRun}
          loading={loading}
          disabled={images.length === 0}
        />
        <ResultsPanel persons={persons} />
      </main>
    </div>
  );
}

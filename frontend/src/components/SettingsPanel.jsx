import { Settings } from 'lucide-react';
import { useState, useEffect } from 'react';
import { getSettings } from '../api';

export default function SettingsPanel({ params, onChange }) {
  const [models, setModels] = useState([]);
  const [detectors, setDetectors] = useState([]);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    getSettings().then((data) => {
      setModels(data.models);
      setDetectors(data.detectors);
    });
  }, []);

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between px-4 py-3 text-sm font-medium text-gray-700 hover:bg-gray-50 rounded-xl transition-colors"
      >
        <span className="flex items-center gap-2">
          <Settings className="w-4 h-4" />
          Analysis Settings
        </span>
        <span className="text-xs text-gray-400">{open ? 'Hide' : 'Show'}</span>
      </button>

      {open && (
        <div className="px-4 pb-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">Model</label>
            <select
              value={params.model_name}
              onChange={(e) => onChange({ ...params, model_name: e.target.value })}
              className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            >
              {models.map((m) => (
                <option key={m} value={m}>{m}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">Detector</label>
            <select
              value={params.detector_backend}
              onChange={(e) => onChange({ ...params, detector_backend: e.target.value })}
              className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            >
              {detectors.map((d) => (
                <option key={d} value={d}>{d}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">
              Distance Threshold: {params.distance_threshold.toFixed(2)}
            </label>
            <input
              type="range"
              min="0.1"
              max="1.0"
              step="0.05"
              value={params.distance_threshold}
              onChange={(e) => onChange({ ...params, distance_threshold: parseFloat(e.target.value) })}
              className="w-full accent-indigo-600"
            />
            <div className="flex justify-between text-[10px] text-gray-400">
              <span>Strict</span>
              <span>Lenient</span>
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-600 mb-1">
              Min Confidence: {params.min_confidence.toFixed(2)}
            </label>
            <input
              type="range"
              min="0.0"
              max="1.0"
              step="0.05"
              value={params.min_confidence}
              onChange={(e) => onChange({ ...params, min_confidence: parseFloat(e.target.value) })}
              className="w-full accent-indigo-600"
            />
            <div className="flex justify-between text-[10px] text-gray-400">
              <span>All faces</span>
              <span>High conf only</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

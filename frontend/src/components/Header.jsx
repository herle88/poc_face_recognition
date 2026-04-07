import { Trash2, ScanFace, Eraser } from 'lucide-react';

export default function Header({ onReset, onClearFaces }) {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <ScanFace className="w-8 h-8 text-indigo-600" />
          <h1 className="text-xl font-semibold text-gray-900">Face Recognition POC</h1>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={onClearFaces}
            className="flex items-center gap-2 px-3 py-2 text-sm text-amber-600 hover:bg-amber-50 rounded-lg transition-colors"
          >
            <Eraser className="w-4 h-4" />
            Clear Faces
          </button>
          <button
            onClick={onReset}
            className="flex items-center gap-2 px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-lg transition-colors"
          >
            <Trash2 className="w-4 h-4" />
            Reset All
          </button>
        </div>
      </div>
    </header>
  );
}

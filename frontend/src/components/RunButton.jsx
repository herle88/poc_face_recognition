import { Loader2, Play } from 'lucide-react';

export default function RunButton({ onRun, loading, disabled }) {
  return (
    <button
      onClick={onRun}
      disabled={disabled || loading}
      className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-medium rounded-xl transition-colors"
    >
      {loading ? (
        <>
          <Loader2 className="w-5 h-5 animate-spin" />
          Analyzing faces...
        </>
      ) : (
        <>
          <Play className="w-5 h-5" />
          Run Analysis
        </>
      )}
    </button>
  );
}

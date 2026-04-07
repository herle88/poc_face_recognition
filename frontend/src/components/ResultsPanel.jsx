import { User } from 'lucide-react';
import { uploadsUrl } from '../api';

const COLORS = [
  'bg-indigo-500', 'bg-emerald-500', 'bg-amber-500', 'bg-rose-500',
  'bg-cyan-500', 'bg-purple-500', 'bg-pink-500', 'bg-teal-500',
];

export default function ResultsPanel({ persons }) {
  if (!persons.length) return null;

  return (
    <div>
      <h2 className="text-lg font-semibold text-gray-900 mb-4">
        Results: {persons.length} unique {persons.length === 1 ? 'person' : 'people'} found
      </h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {persons.map((person, idx) => (
          <div key={person.id} className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
            <div className="flex items-center gap-3 mb-3">
              <div className={`w-10 h-10 rounded-full ${COLORS[idx % COLORS.length]} flex items-center justify-center`}>
                <User className="w-5 h-5 text-white" />
              </div>
              <div>
                <h3 className="font-medium text-gray-900">{person.label}</h3>
                <p className="text-xs text-gray-500">
                  {person.faces.length} {person.faces.length === 1 ? 'image' : 'images'}
                </p>
              </div>
            </div>
            <div className="grid grid-cols-3 gap-2">
              {person.faces.map((face) => (
                <img
                  key={face.face_id}
                  src={uploadsUrl(face.filename)}
                  alt={face.original_name}
                  title={face.original_name}
                  className="w-full aspect-square object-cover rounded-lg"
                />
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

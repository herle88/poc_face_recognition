import { uploadsUrl } from '../api';

export default function ImageGrid({ images }) {
  if (!images.length) return null;

  return (
    <div>
      <h2 className="text-sm font-medium text-gray-700 mb-2">
        Uploaded Images ({images.length})
      </h2>
      <div className="grid grid-cols-4 sm:grid-cols-6 lg:grid-cols-8 gap-2">
        {images.map((img) => (
          <div key={img.id} className="relative group">
            <img
              src={uploadsUrl(img.filename)}
              alt={img.original_name}
              className="w-full aspect-square object-cover rounded-lg"
            />
            <div className="absolute inset-x-0 bottom-0 bg-black/50 text-white text-[10px] px-1 py-0.5 rounded-b-lg truncate opacity-0 group-hover:opacity-100 transition-opacity">
              {img.original_name}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

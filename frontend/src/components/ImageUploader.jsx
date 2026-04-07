import { useState, useRef } from 'react';
import { Upload } from 'lucide-react';
import { uploadImages } from '../api';

export default function ImageUploader({ onUpload }) {
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const inputRef = useRef(null);

  const handleFiles = async (files) => {
    if (!files.length) return;
    setUploading(true);
    try {
      const data = await uploadImages(Array.from(files));
      onUpload(data.images);
    } catch (e) {
      console.error('Upload error:', e);
    } finally {
      setUploading(false);
    }
  };

  const onDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    handleFiles(e.dataTransfer.files);
  };

  return (
    <div
      onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
      onDragLeave={() => setDragging(false)}
      onDrop={onDrop}
      onClick={() => inputRef.current?.click()}
      className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors ${
        dragging ? 'border-indigo-500 bg-indigo-50' : 'border-gray-300 hover:border-gray-400'
      }`}
    >
      <input
        ref={inputRef}
        type="file"
        multiple
        accept="image/*"
        className="hidden"
        onChange={(e) => handleFiles(e.target.files)}
      />
      <Upload className="w-10 h-10 mx-auto text-gray-400 mb-3" />
      {uploading ? (
        <p className="text-sm text-gray-500">Uploading...</p>
      ) : (
        <>
          <p className="text-sm font-medium text-gray-700">Drop images here or click to browse</p>
          <p className="text-xs text-gray-400 mt-1">Supports JPG, PNG, WebP</p>
        </>
      )}
    </div>
  );
}

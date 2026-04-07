// Detect HA ingress base path from URL (e.g. /api/hassio_ingress/xxx/)
// In dev mode or standalone, this is empty string
function getBasePath() {
  const match = window.location.pathname.match(/^(\/api\/hassio_ingress\/[^/]+)/);
  return match ? match[1] : '';
}

const BASE = `${getBasePath()}/api`;

export function uploadsUrl(filename) {
  return `${getBasePath()}/uploads/${filename}`;
}

export async function uploadImages(files) {
  const form = new FormData();
  files.forEach((f) => form.append('files', f));
  const res = await fetch(`${BASE}/upload`, { method: 'POST', body: form });
  if (!res.ok) throw new Error('Upload failed');
  return res.json();
}

export async function runAnalysis(params = {}) {
  const res = await fetch(`${BASE}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params),
  });
  if (!res.ok) throw new Error('Analysis failed');
  return res.json();
}

export async function getResults() {
  const res = await fetch(`${BASE}/results`);
  if (!res.ok) throw new Error('Failed to fetch results');
  return res.json();
}

export async function getSettings() {
  const res = await fetch(`${BASE}/settings`);
  if (!res.ok) throw new Error('Failed to fetch settings');
  return res.json();
}

export async function clearFaces() {
  const res = await fetch(`${BASE}/faces`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Clear faces failed');
  return res.json();
}

export async function resetAll() {
  const res = await fetch(`${BASE}/reset`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Reset failed');
  return res.json();
}

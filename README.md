# DeepFace Recognition

Face recognition tool that groups images by unique person. Upload a batch of photos, run analysis, and get back clusters of images belonging to the same person.

Powered by [DeepFace](https://github.com/serengil/deepface). Available as a standalone web app or a Home Assistant add-on.

## Features

- Drag-and-drop image upload
- Multiple face recognition models (VGG-Face, Facenet, ArcFace, etc.)
- Multiple face detectors (opencv, mtcnn, retinaface, ssd)
- Tunable distance threshold and confidence filter
- Results displayed as person cards with grouped thumbnails

## Tech Stack

- **Backend**: Python 3.11, FastAPI, DeepFace, SQLite
- **Frontend**: React 18, Vite, Tailwind CSS, Lucide icons

## Quick Start (Development)

```bash
# Backend
cd backend
/opt/homebrew/bin/python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## Home Assistant Add-on

1. Push this repo to GitHub
2. In Home Assistant go to **Settings > Add-ons > Add-on Store**
3. Open the three-dot menu, select **Repositories**, and add the repo URL
4. Install **DeepFace Recognition** and start it
5. Click **Open Web UI**

Data persists in the add-on's `/data` directory across restarts.

## Usage

1. Upload images using drag-and-drop or the file picker
2. Open **Analysis Settings** to adjust model, detector, and thresholds
3. Click **Run Analysis**
4. Results show person cards, each with the grouped images

The first run downloads the selected model (~500MB for VGG-Face).

## Project Structure

```
├── backend/
│   ├── main.py              # FastAPI app
│   ├── database.py          # SQLite schema and queries
│   ├── routers/api.py       # API endpoints
│   └── services/
│       ├── face_service.py  # DeepFace wrapper
│       └── clustering.py    # Union-Find cosine similarity clustering
├── frontend/
│   └── src/
│       ├── App.jsx          # Main app
│       ├── api.js           # API client
│       └── components/      # UI components
├── Dockerfile               # Multi-stage build for HA add-on
├── config.yaml              # HA add-on configuration
├── rootfs/run.sh            # Add-on entry point
└── repository.json          # HA add-on repository metadata
```

import json
import os
import uuid
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Query
from pydantic import BaseModel

from database import (
    UPLOADS_DIR,
    insert_image,
    get_pending_images,
    update_image_status,
    insert_face,
    get_all_faces,
    clear_faces,
    clear_person_groups,
    insert_person,
    link_face_person,
    get_results,
    reset_all,
)
from services.face_service import extract_faces, MODELS, DETECTORS
from services.clustering import cluster_faces

router = APIRouter()


class AnalyzeParams(BaseModel):
    model_name: str = "VGG-Face"
    detector_backend: str = "opencv"
    distance_threshold: float = 0.55
    min_confidence: float = 0.5


@router.get("/settings")
async def get_settings():
    return {
        "models": MODELS,
        "detectors": DETECTORS,
        "defaults": {
            "model_name": "VGG-Face",
            "detector_backend": "opencv",
            "distance_threshold": 0.55,
            "min_confidence": 0.5,
        },
    }


@router.post("/upload")
async def upload_images(files: list[UploadFile] = File(...)):
    uploaded = []
    for f in files:
        ext = os.path.splitext(f.filename or "image.jpg")[1] or ".jpg"
        filename = f"{uuid.uuid4().hex}{ext}"
        filepath = os.path.join(UPLOADS_DIR, filename)
        content = await f.read()
        with open(filepath, "wb") as out:
            out.write(content)
        image_id = insert_image(filename, f.filename or "unknown")
        uploaded.append({"id": image_id, "filename": filename, "original_name": f.filename})
    return {"images": uploaded}


@router.delete("/faces")
async def clear_faces_endpoint():
    clear_faces()
    return {"status": "ok"}


@router.post("/analyze")
async def analyze(params: AnalyzeParams = AnalyzeParams()):
    clear_faces()
    pending = get_pending_images()
    processed_count = 0
    error_count = 0

    for img in pending:
        filepath = os.path.join(UPLOADS_DIR, img["filename"])
        try:
            faces = extract_faces(
                filepath,
                model_name=params.model_name,
                detector_backend=params.detector_backend,
            )
            # Keep only the best face detection per image
            if faces:
                best = max(faces, key=lambda f: f["confidence"])
                insert_face(
                    image_id=img["id"],
                    embedding=json.dumps(best["embedding"]),
                    facial_area=json.dumps(best["facial_area"]),
                    confidence=best["confidence"],
                )
            update_image_status(img["id"], "processed")
            processed_count += 1
        except Exception as e:
            update_image_status(img["id"], "error")
            error_count += 1
            print(f"Error processing {img['filename']}: {e}")

    # Cluster all faces, filtering by minimum confidence
    all_faces = get_all_faces()
    face_data = [
        {"id": f["id"], "embedding": json.loads(f["embedding"])}
        for f in all_faces
        if f["confidence"] >= params.min_confidence
    ]
    groups = cluster_faces(face_data, threshold=params.distance_threshold)

    # Save person groups
    clear_person_groups()
    for i, group in enumerate(groups):
        person_id = insert_person(f"Person {i + 1}")
        for face_id in group:
            link_face_person(face_id, person_id)

    results = get_results()
    return {
        "processed": processed_count,
        "errors": error_count,
        "persons": results,
    }


@router.get("/results")
async def results():
    return {"persons": get_results()}


@router.delete("/reset")
async def reset():
    reset_all()
    return {"status": "ok"}

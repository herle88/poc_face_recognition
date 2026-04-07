from deepface import DeepFace

MODELS = ["VGG-Face", "Facenet", "Facenet512", "ArcFace", "SFace", "OpenFace", "DeepID", "Dlib"]
DETECTORS = ["opencv", "mtcnn", "retinaface", "ssd"]


def extract_faces(image_path: str, model_name: str = "VGG-Face", detector_backend: str = "opencv") -> list[dict]:
    """Extract face embeddings from an image. Returns list of {embedding, facial_area, confidence}."""
    results = DeepFace.represent(
        img_path=image_path,
        model_name=model_name,
        enforce_detection=False,
        detector_backend=detector_backend,
    )
    return [
        {
            "embedding": r["embedding"],
            "facial_area": r["facial_area"],
            "confidence": r.get("face_confidence", 0.0),
        }
        for r in results
    ]

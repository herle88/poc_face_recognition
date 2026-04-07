import sqlite3
import os
import shutil

# Use /data for HA add-on persistent storage, fallback to local for dev
DATA_DIR = os.environ.get("DATA_DIR", os.path.dirname(__file__))
DB_PATH = os.path.join(DATA_DIR, "face_recognition.db")
UPLOADS_DIR = os.path.join(DATA_DIR, "uploads")


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            original_name TEXT NOT NULL,
            upload_time TEXT DEFAULT (datetime('now')),
            status TEXT DEFAULT 'pending'
        );
        CREATE TABLE IF NOT EXISTS faces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_id INTEGER NOT NULL REFERENCES images(id) ON DELETE CASCADE,
            embedding TEXT NOT NULL,
            facial_area TEXT,
            confidence REAL
        );
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT
        );
        CREATE TABLE IF NOT EXISTS face_person (
            face_id INTEGER NOT NULL REFERENCES faces(id) ON DELETE CASCADE,
            person_id INTEGER NOT NULL REFERENCES persons(id) ON DELETE CASCADE,
            PRIMARY KEY (face_id, person_id)
        );
    """)
    conn.close()


def insert_image(filename: str, original_name: str) -> int:
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO images (filename, original_name) VALUES (?, ?)",
        (filename, original_name),
    )
    conn.commit()
    image_id = cur.lastrowid
    conn.close()
    return image_id


def insert_face(image_id: int, embedding: str, facial_area: str, confidence: float) -> int:
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO faces (image_id, embedding, facial_area, confidence) VALUES (?, ?, ?, ?)",
        (image_id, embedding, facial_area, confidence),
    )
    conn.commit()
    face_id = cur.lastrowid
    conn.close()
    return face_id


def get_pending_images() -> list[dict]:
    conn = get_db()
    rows = conn.execute("SELECT id, filename, original_name FROM images WHERE status = 'pending'").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_image_status(image_id: int, status: str):
    conn = get_db()
    conn.execute("UPDATE images SET status = ? WHERE id = ?", (status, image_id))
    conn.commit()
    conn.close()


def get_all_faces() -> list[dict]:
    conn = get_db()
    rows = conn.execute("SELECT id, image_id, embedding, facial_area, confidence FROM faces").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def insert_person(label: str) -> int:
    conn = get_db()
    cur = conn.execute("INSERT INTO persons (label) VALUES (?)", (label,))
    conn.commit()
    person_id = cur.lastrowid
    conn.close()
    return person_id


def link_face_person(face_id: int, person_id: int):
    conn = get_db()
    conn.execute("INSERT INTO face_person (face_id, person_id) VALUES (?, ?)", (face_id, person_id))
    conn.commit()
    conn.close()


def clear_faces():
    conn = get_db()
    conn.executescript("""
        DELETE FROM face_person;
        DELETE FROM persons;
        DELETE FROM faces;
        UPDATE images SET status = 'pending';
    """)
    conn.close()


def clear_person_groups():
    conn = get_db()
    conn.execute("DELETE FROM face_person")
    conn.execute("DELETE FROM persons")
    conn.commit()
    conn.close()


def get_results() -> list[dict]:
    conn = get_db()
    rows = conn.execute("""
        SELECT p.id as person_id, p.label,
               f.id as face_id, f.facial_area, f.confidence,
               i.id as image_id, i.filename, i.original_name
        FROM persons p
        JOIN face_person fp ON fp.person_id = p.id
        JOIN faces f ON f.id = fp.face_id
        JOIN images i ON i.id = f.image_id
        ORDER BY p.id, f.id
    """).fetchall()
    conn.close()

    persons = {}
    for r in rows:
        r = dict(r)
        pid = r["person_id"]
        if pid not in persons:
            persons[pid] = {"id": pid, "label": r["label"], "faces": []}
        persons[pid]["faces"].append({
            "face_id": r["face_id"],
            "image_id": r["image_id"],
            "filename": r["filename"],
            "original_name": r["original_name"],
            "facial_area": r["facial_area"],
            "confidence": r["confidence"],
        })
    return list(persons.values())


def reset_all():
    conn = get_db()
    conn.executescript("""
        DELETE FROM face_person;
        DELETE FROM faces;
        DELETE FROM persons;
        DELETE FROM images;
    """)
    conn.close()
    if os.path.exists(UPLOADS_DIR):
        shutil.rmtree(UPLOADS_DIR)
    os.makedirs(UPLOADS_DIR, exist_ok=True)

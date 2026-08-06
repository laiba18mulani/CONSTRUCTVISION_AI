"""SQLite reference store. Replace its connection URL with Postgres/Timescale in deployment."""
from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "twin_platform.db"


@contextmanager
def connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    try:
        yield db
        db.commit()
    finally:
        db.close()


def initialize() -> None:
    with connection() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS assets (id TEXT PRIMARY KEY, name TEXT NOT NULL, location TEXT, created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS captures (id TEXT PRIMARY KEY, asset_id TEXT NOT NULL, image_count INTEGER NOT NULL, calibration_json TEXT, state TEXT NOT NULL, created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS telemetry (id TEXT PRIMARY KEY, asset_id TEXT NOT NULL, sensor_id TEXT NOT NULL, measured_at TEXT NOT NULL, metric TEXT NOT NULL, value REAL NOT NULL, unit TEXT NOT NULL, quality TEXT NOT NULL, metadata_json TEXT);
        CREATE INDEX IF NOT EXISTS telemetry_asset_time ON telemetry(asset_id, measured_at);
        CREATE TABLE IF NOT EXISTS analysis_jobs (id TEXT PRIMARY KEY, asset_id TEXT NOT NULL, kind TEXT NOT NULL, state TEXT NOT NULL, inputs_json TEXT NOT NULL, artifact_uri TEXT, message TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
        """)


def create_asset(name: str, location: str | None, created_at: str) -> dict:
    asset = {"id": str(uuid4()), "name": name, "location": location, "created_at": created_at}
    with connection() as db:
        db.execute("INSERT INTO assets VALUES (:id,:name,:location,:created_at)", asset)
    return asset


def create_capture(asset_id: str, image_count: int, calibration: dict, created_at: str) -> dict:
    item = {"id": str(uuid4()), "asset_id": asset_id, "image_count": image_count, "calibration_json": json.dumps(calibration), "state": "QUEUED", "created_at": created_at}
    with connection() as db:
        db.execute("INSERT INTO captures VALUES (:id,:asset_id,:image_count,:calibration_json,:state,:created_at)", item)
    return {**item, "calibration": calibration}


def insert_telemetry(asset_id: str, samples: list[dict]) -> int:
    with connection() as db:
        db.executemany("INSERT INTO telemetry VALUES (:id,:asset_id,:sensor_id,:measured_at,:metric,:value,:unit,:quality,:metadata_json)", samples)
    return len(samples)


def create_job(asset_id: str, kind: str, inputs: dict, now: str) -> dict:
    item = {"id": str(uuid4()), "asset_id": asset_id, "kind": kind, "state": "QUEUED", "inputs_json": json.dumps(inputs), "artifact_uri": None, "message": None, "created_at": now, "updated_at": now}
    with connection() as db:
        db.execute("INSERT INTO analysis_jobs VALUES (:id,:asset_id,:kind,:state,:inputs_json,:artifact_uri,:message,:created_at,:updated_at)", item)
    return {**item, "inputs": inputs}


def get_job(job_id: str) -> dict | None:
    with connection() as db:
        row = db.execute("SELECT * FROM analysis_jobs WHERE id=?", (job_id,)).fetchone()
    if not row:
        return None
    item = dict(row)
    item["inputs"] = json.loads(item.pop("inputs_json"))
    return item


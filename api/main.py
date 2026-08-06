"""Product API: asset registry, calibrated capture intake, IoT data and solver jobs."""
from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status

from platform_core.contracts import AnalysisRequest, AssetCreate, CaptureCreate, TelemetryBatch
from platform_core.store import create_asset, create_capture, create_job, get_job, initialize, insert_telemetry
from workers.dispatcher import solver_readiness

app = FastAPI(title="ConstructVision Digital Twin API", version="2.0.0", description="API-first platform for image reconstruction, IoT monitoring and engineering solver workflows.")


@app.on_event("startup")
def startup() -> None:
    initialize()


@app.get("/health")
def health() -> dict:
    return {"service": "constructvision-api", "status": "ok", "time": datetime.now(timezone.utc).isoformat()}


@app.post("/v1/assets", status_code=status.HTTP_201_CREATED)
def register_asset(payload: AssetCreate) -> dict:
    return create_asset(payload.name, payload.location, datetime.now(timezone.utc).isoformat())


@app.post("/v1/captures", status_code=status.HTTP_202_ACCEPTED)
def register_capture(payload: CaptureCreate) -> dict:
    calibration = {"image_manifest_uri": payload.image_manifest_uri, "calibrated": payload.calibrated, "scale_reference_m": payload.scale_reference_m}
    capture = create_capture(str(payload.asset_id), payload.image_count, calibration, datetime.now(timezone.utc).isoformat())
    readiness = solver_readiness("RECONSTRUCTION")
    return {"capture": capture, "reconstruction_worker": readiness, "capture_guidance": "Use 60+ overlapping images and scale control for metric reconstruction; three oblique images are reference-only."}


@app.post("/v1/telemetry:ingest", status_code=status.HTTP_202_ACCEPTED)
def ingest_telemetry(payload: TelemetryBatch) -> dict:
    samples = [{"id": str(uuid4()), "asset_id": str(payload.asset_id), "sensor_id": item.sensor_id, "measured_at": item.measured_at.astimezone(timezone.utc).isoformat(), "metric": item.metric, "value": item.value, "unit": item.unit, "quality": item.quality, "metadata_json": str(item.metadata)} for item in payload.samples]
    return {"accepted": insert_telemetry(str(payload.asset_id), samples), "asset_id": str(payload.asset_id)}


@app.post("/v1/analysis-jobs", status_code=status.HTTP_202_ACCEPTED)
def queue_analysis(payload: AnalysisRequest) -> dict:
    job = create_job(str(payload.asset_id), payload.kind.value, {"model_revision": payload.model_revision, **payload.inputs}, datetime.now(timezone.utc).isoformat())
    return {"job": job, "worker": solver_readiness(payload.kind.value), "note": "Job remains blocked until the named solver worker is installed and configured; the API never substitutes cosmetic output for a solver result."}


@app.get("/v1/analysis-jobs/{job_id}")
def read_job(job_id: str) -> dict:
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Analysis job not found")
    return job

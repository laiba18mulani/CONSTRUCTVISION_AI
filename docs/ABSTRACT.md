# ConstructVision AI: Abstract

ConstructVision AI is a built-environment intelligence project that explores how computer vision, digital-twin workflows and operational data can support construction inspection. The project provides a portfolio-facing landing experience and a Streamlit workspace for asset context, parametric 3D frame visualisation, capture intake, asset-health views and deployment/solver integration status. A FastAPI service provides typed contracts for asset registration, calibrated image-capture packages, telemetry ingestion and analysis-job requests.

The central design principle is that a visual model must not be mistaken for engineering evidence. The current prototype demonstrates preliminary screening and workflow orchestration only. It records the distinction between a parametric view, a calibrated reconstruction, and an engineer-reviewed finite-element or CFD result. Solver-backed capabilities are exposed only when the required workers are available; otherwise jobs remain blocked rather than returning fabricated results.

The proposed production path uses managed PostgreSQL/TimescaleDB, object storage, secure telemetry ingestion, durable background jobs and isolated reconstruction/analysis workers. ConstructVision AI therefore positions AI as an assistive layer for evidence organisation, inspection triage and communication, while retaining human accountability for safety-critical decisions.

**Keywords:** digital twin, construction inspection, computer vision, structural health monitoring, 3D visualisation, engineering workflow, FastAPI, Streamlit.

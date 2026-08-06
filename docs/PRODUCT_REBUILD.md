# ConstructVision Digital Twin — product rebuild

## Product definition

ConstructVision is an API-first built-asset digital-twin platform. A visual client is only one consumer of the system—not the product itself. The source of truth is a versioned asset model, calibrated capture evidence, telemetry history, analysis inputs, solver outputs and engineer sign-off.

## System boundary

```text
Site capture / BIM / drawings ──> reconstruction worker ──> versioned geometry & material model
IoT devices ──> secure gateway / MQTT ──> telemetry API ──> time-series store / anomaly service
Twin revision + scenario ──> FEA / CFD / flood workers ──> immutable result artifacts ──> review workflow
```

## Delivered foundation

- `api/`: FastAPI service for asset registration, capture packages, telemetry intake and analysis job contracts.
- `platform_core/`: persistent domain storage and typed contracts; SQLite is the local reference implementation and PostgreSQL/Timescale is the deployment target.
- `workers/`: explicit capability checks for COLMAP, OpenSees and OpenFOAM. A job is blocked when a solver is absent—never replaced with an invented result.

## Non-negotiable engineering rules

1. Three images are not treated as metric geometry. Reconstruction must preserve camera calibration, scale control, coverage metrics and uncertainty.
2. Every analysis references a specific model revision, materials, loads, mesh/solver settings and result artifact checksum.
3. Telemetry retains UTC timestamp, unit, quality flag, device identity and raw payload provenance.
4. FEA, CFD and flood runs execute in isolated workers with solver/version logs. UI animations are never engineering evidence.
5. Design decisions require a licensed engineer’s review and sign-off.

## Build sequence

1. Replace SQLite with PostgreSQL + TimescaleDB and object storage.
2. Deploy MQTT gateway with mTLS, per-device credentials and a schema registry.
3. Containerize COLMAP/OpenMVS for reconstruction; emit mesh + sparse/dense cloud QA artifacts.
4. Add a BIM/IFC import service and mesh-to-semantic element registration.
5. Deploy OpenSees and OpenFOAM workers with durable queues, scenario templates and artifact retention.
6. Build the web/3D client only after these contracts are stable. It should consume glTF/3D Tiles plus approved result fields.

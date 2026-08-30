# Evidence matrix

| Requested capability | Evidence in checkout | Documentation treatment |
| --- | --- | --- |
| YOLOv8 detection | Settings page names YOLOv8-X/N, but no model-loading or inference call exists; `models/yolov11.pt` is present. | Proposed production architecture; current prototype uses OpenCV Canny/contours. |
| Defect inspection | `pages/5_🔬_AI_Inspection.py` performs grayscale conversion, Gaussian blur, Canny edges, contour filtering, pixel-to-mm conversion and rule-based severity. | Implemented and mathematically documented. |
| 3D twin | `pages/7_🏗️_3D_Building.py` contains a parameterized Three.js viewer; `app.py` contains a Plotly frame viewer. | Implemented visual prototype. |
| Structural screening | `modules/digital_twin/engine.py` calculates tributary gravity, axial stress, simple beam moment/stress, wind pressure, hydrostatic pressure and utilization. | Implemented preliminary screening only. |
| 4D seismic | UI label `Seismic Oscillation` exists, but no seismic equation or time-history solver is implemented. | Proposed extension with equations, explicitly not a measured result. |
| ESG carbon forecast | No carbon/emission logic found in source. | Proposed lifecycle-accounting extension, not a project result. |
| IoT/telemetry | Demo sensor data in page 3; deterministic synthetic telemetry in `engine.py`; typed telemetry contracts in `platform_core/contracts.py`. | Implemented demo/contracts; production ingestion remains future work. |
| Cost estimation | `pages/9_💰_Cost_Estimation.py` implements material, labour, scaffolding, GST and quantity calculations. | Implemented formulae reproduced. |
| Solver integration | `workers/dispatcher.py` checks COLMAP/OpenSees/OpenFOAM availability and returns READY/BLOCKED. | Implemented readiness boundary; no solver output fabricated. |

## Project analysis summary

ConstructVision AI is best understood as an **inspection-workflow and decision-support prototype**. Its immediate strength is not a trained artificial-intelligence model or a certified structural analysis result. Its strength is the attempt to keep a field observation, its approximate measurement, its asset context, a transparent preliminary check, a recommended workflow and a report in one place.

The checkout has two user-interface layers. The root `app.py` provides the newer operational command centre: portfolio, twin studio, capture and reconstruction, health, telemetry and integration views. The `pages/` directory remains a richer prototype library for tutorial, virtual practical, GPS, inspection, damage analysis, 3D building, IoT, cost, materials, history, reports and configuration. `platform_core/` and `workers/` provide a deliberately small API-oriented foundation for a future service architecture.

## Verified source inventory

| Area | Primary source files | What is demonstrably present | Important boundary |
| --- | --- | --- | --- |
| Application shell | `main.py`, `app.py`, `modules/portfolio.py` | Streamlit entry point, operational navigation, Plotly frame visualisation and command-centre screens. | Presentation is local/prototype; no production authentication boundary is evidenced here. |
| Image triage | `pages/5_🔬_AI_Inspection.py`, `modules/ai_detection.py`, `modules/inspection/` | Image upload, OpenCV-style inspection workflow and rule-based severity support. | A contour/heuristic result is not a calibrated defect diagnosis. |
| Structural context | `pages/7_🏗️_3D_Building.py`, `modules/digital_twin/engine.py`, `modules/building/` | Parametric geometry, frame nodes/members and simple mechanical indicators. | No code-compliant design, FEA result or calibrated as-built model is established. |
| Telemetry | `pages/8_📡_IoT.py`, `modules/iot/monitor.py`, `modules/sensor_state.py`, `platform_core/contracts.py` | Demonstration channels, synthetic telemetry and validation models for telemetry records. | No live gateway, device identity, time-series database or alert-delivery evidence is recorded. |
| Repair workflow | `pages/6_📊_Damage_Analysis.py`, `pages/9_💰_Cost_Estimation.py`, `modules/cost/` | Repair/risk presentation, BOQ-style calculation and cost components. | Costs are planning estimates; site measurement, supplier quotation and engineer approval remain required. |
| Reporting and history | `pages/11_📂_History.py`, `pages/12_📄_Reports.py`, `modules/reports.py`, `modules/history/` | User-facing inspection history and report-generation workflow. | Immutable evidence storage, signatures and retention enforcement are future controls. |
| External analysis | `workers/dispatcher.py` | Explicit COLMAP, OpenSees and OpenFOAM readiness checks. | `BLOCKED` means no analysis has run; no result should be inferred. |

## Claim-control register

| Claim category | Wording allowed in the current documentation | Wording to avoid until validation exists | Evidence needed to promote the claim |
| --- | --- | --- | --- |
| AI defect detection | “Rule-based/OpenCV-assisted image triage” | “YOLOv8 detects defects with X% accuracy” | Versioned dataset, model checkpoint, held-out evaluation and error analysis. |
| Crack dimensions | “Approximate dimensions derived from a user-supplied scale” | “Metric crack measurement” | Calibrated capture protocol, reference targets and measurement-error study. |
| 3D twin | “Parametric visual twin” | “As-built BIM/digital twin” | Survey control, reconstruction report, model revision and spatial accuracy results. |
| Structural result | “Preliminary transparent screening indicator” | “Safe”, “approved”, “code compliant” or “design verified” | Governing design basis, load combinations, validated model and licensed engineer sign-off. |
| Sensor monitoring | “Synthetic/demo telemetry and typed record contract” | “Live monitoring” or “real-time alerts” | Device inventory, gateway logs, timestamp checks, data-quality report and alert audit trail. |
| Cost estimate | “Illustrative BOQ-style estimate” | “Final project cost” | Measured quantities, approved scope, vendor rates, tax treatment and approval record. |

## Evidence package required for a field pilot

Before a field pilot, retain a per-inspection evidence package containing the following items:

1. Asset identifier, site/location reference, component identifier and inspection purpose.
2. Original image/video files, capture timestamp, camera/device details and consent/access record.
3. Calibration target or scale method, estimated measurement uncertainty and any image pre-processing record.
4. Detector or rule-set revision, thresholds, raw outputs, reviewed outputs and reviewer identity.
5. Sensor identifier, unit, time zone/UTC timestamp, quality flag, missing-data handling and calibration status.
6. Structural-screening inputs, units, assumptions, result revision and the explicit preliminary-result warning.
7. Repair recommendation, cost assumptions, exclusions, approvals and final report version.

## Documentation maintenance rules

- Refer to the actual current page names: `pages/5_🔬_AI_Inspection.py`, `pages/7_🏗️_3D_Building.py` and `pages/9_💰_Cost_Estimation.py`.
- Put measured results in a dated test record; keep targets and illustrative values labelled as targets.
- Update this matrix whenever a model, dataset, sensor connection, solver worker or report-signing workflow changes.
- Preserve the distinction between implemented, demo/synthetic, readiness-only and proposed capabilities in every presentation and report.

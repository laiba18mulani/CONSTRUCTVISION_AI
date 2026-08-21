# Evidence matrix

| Requested capability | Evidence in checkout | Documentation treatment |
| --- | --- | --- |
| YOLOv8 detection | Settings page names YOLOv8-X/N, but no model-loading or inference call exists; `models/yolov11.pt` is present. | Proposed production architecture; current prototype uses OpenCV Canny/contours. |
| Defect inspection | `pages/6_🔬_AI_Inspection.py` performs grayscale conversion, Gaussian blur, Canny edges, contour filtering, pixel-to-mm conversion and rule-based severity. | Implemented and mathematically documented. |
| 3D twin | `pages/3_🏗️_3D_Building.py` contains a parameterized Three.js viewer; `app.py` contains a Plotly frame viewer. | Implemented visual prototype. |
| Structural screening | `modules/digital_twin/engine.py` calculates tributary gravity, axial stress, simple beam moment/stress, wind pressure, hydrostatic pressure and utilization. | Implemented preliminary screening only. |
| 4D seismic | UI label `Seismic Oscillation` exists, but no seismic equation or time-history solver is implemented. | Proposed extension with equations, explicitly not a measured result. |
| ESG carbon forecast | No carbon/emission logic found in source. | Proposed lifecycle-accounting extension, not a project result. |
| IoT/telemetry | Demo sensor data in page 3; deterministic synthetic telemetry in `engine.py`; typed telemetry contracts in `platform_core/contracts.py`. | Implemented demo/contracts; production ingestion remains future work. |
| Cost estimation | `pages/8_💰_Cost_Estimation.py` implements material, labour, scaffolding, GST and quantity calculations. | Implemented formulae reproduced. |
| Solver integration | `workers/dispatcher.py` checks COLMAP/OpenSees/OpenFOAM availability and returns READY/BLOCKED. | Implemented readiness boundary; no solver output fabricated. |

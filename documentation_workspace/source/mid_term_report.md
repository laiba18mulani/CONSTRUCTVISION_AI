# CONSTRUCTVISION AI

## Evidence-First Civil Infrastructure Inspection and Digital-Twin Prototype

| Particular | Details |
| --- | --- |
| Document code | MTR-2026-CE-001-002 |
| Academic program | Engineering Internship Project, Diploma in Civil Engineering |
| Affiliation | Department of Civil Engineering |
| Industry partner | Chatake Innoworks Pvt. Ltd., MindForgeAI Division, Solapur, Maharashtra |
| Project timeline | August 2026, four-week internship prototype |
| Authors | Ritika Bhumkar (Reg. No. 2026CE001); Laiba Mulani (Reg. No. 2026CE002) |
| Academic supervisor | Ms. Swati P. Maniyal, M.TECH, Structural Engineering |
| Industry guide | Mr. Akash S. Chatake, M.TECH, AIML, BITS Pilani |

> **MID-TERM STATUS:** This report records the engineering state at the mid-term checkpoint. Completed, demonstration, readiness-only, in-progress and planned capabilities are intentionally separated. A roadmap item is not represented as a completed result.

## Executive Summary

ConstructVision AI is being developed as an evidence-first civil-infrastructure inspection and site-intelligence prototype. The central aim is to create one reviewable workflow in which an inspection image, asset context, preliminary measurement, structural-screening indicator, repair estimate and report can remain connected. Instead of treating a 3D visualisation or automatic flag as a final engineering answer, the project makes assumptions, source evidence, uncertainty and review boundaries visible.

At this mid-term checkpoint, the project has progressed from requirements analysis into an integrated Streamlit prototype. The current checkout includes a rule-based OpenCV image-triage workflow, parametric frame visualisation, deterministic synthetic telemetry, transparent preliminary structural screening, cost and report workflows, typed data contracts, local reference storage and external solver-readiness checks. The project is now positioned between prototype integration and evidence-based validation.

## 1. Introduction

### 1.1 Project Background

Civil assets are affected by visual deterioration, environmental loading, maintenance history and changing operational conditions. Images, notes, component information, cost estimates and sensor readings are often held separately, making later review difficult. A digital-twin-oriented workflow can provide valuable context when it links evidence to a component, model revision, method and reviewer.

### 1.2 Problem Statement

The engineering problem is to build an understandable inspection workflow that connects heterogeneous evidence—field photographs, approximate measurements, component context, telemetry concepts and repair estimates—to a reviewable decision. The challenge is not only user-interface development; it includes evidence quality, calibration, data validation, transparent calculations, careful claim control and the safe handoff to qualified engineers.

### 1.3 Objectives

- Establish an integrated Streamlit workspace for inspection, visual context, preliminary screening and reporting.
- Use transparent rule-based image processing to triage visible image features.
- Provide a parameterised structural-frame view and synthetic telemetry for prototype demonstration.
- Preserve validated data contracts for future assets, captures, telemetry and analysis jobs.
- Separate preliminary screening and worker readiness from validated structural analysis.
- Demonstrate a traceable path from capture through review, cost and report.

## 2. Infrastructure Problem and Domain Analysis

Infrastructure condition is multi-dimensional: an observed crack may be influenced by material condition, loading, environment and construction history. A useful system must therefore preserve the original evidence and explain how any result was obtained. The ConstructVision AI prototype treats the physical asset, its visual evidence, spatial context and monitoring concepts as related but distinct records.

The parametric twin gives visual component context. The image workflow supplies a visible-feature triage result. Synthetic telemetry supports interface and trend demonstrations. Preliminary mechanics provide an explicit first-pass indicator. Repair-cost and reporting modules connect these inputs to an action-oriented workflow. Human engineering review remains the decision point for safety-critical action.

## 3. Research and Requirement Engineering

| Requirement area | Mid-term interpretation | Status |
| --- | --- | --- |
| Asset and capture context | Asset name/location and capture metadata require a structured record. | **Completed — contract level** |
| Image triage | Uploaded/camera/demo imagery is processed with OpenCV rules and a user-supplied scale. | **Completed — prototype** |
| Spatial context | A parameterised frame and 3D building view provide component context. | **Completed — visual prototype** |
| Telemetry | Demonstration telemetry and typed samples are required before live integration. | **Completed — synthetic/contracts** |
| Screening | Gravity, flexure, wind and flood indicators must show assumptions and a review threshold. | **Completed — preliminary only** |
| Reporting and costing | Inspection findings should feed illustrative repair and report workflows. | **Completed — prototype** |
| External solvers | Reconstruction, FEA and CFD requests must never fabricate a result when unavailable. | **Completed — readiness boundary** |
| Field validation | Calibrated capture, labelled data, benchmark metrics and engineer review are required. | **In progress / planned** |
| Production security and integration | Authentication, immutable storage, live MQTT/API ingestion and durable queues are required. | **Planned** |

## 4. System Architecture and Data Strategy

```text
Capture image / field note / telemetry sample
                 |
                 v
         Metadata and contract validation
                 |
       +---------+----------+----------------+
       v                    v                v
Image triage        Parametric twin    Telemetry quality
       |                    |                |
       +---------+----------+----------------+
                 v
    Preliminary screening and engineer review
                 |
                 v
    Repair estimate, report and audit record
                 |
                 v
  Optional external worker: READY or BLOCKED
```

The data strategy separates implemented prototype data from future production data. `platform_core/contracts.py` specifies typed asset, capture, telemetry and analysis-request records. `platform_core/store.py` supplies local SQLite reference storage. `modules/digital_twin/engine.py` creates deterministic synthetic telemetry for demonstrations. In a production system, object storage, authenticated ingestion, time-series persistence, immutable manifests and versioned worker artifacts are required.

## 5. Implementation Progress

### 5.1 Image inspection workflow

The active inspection page accepts a camera frame, uploaded field image or synthetic concrete target. It uses grayscale/HSV processing, optional sky/glare and vegetation suppression, Gaussian blur, Canny edges, morphological closing and contour filtering. Approximate length and width are calculated from a user-supplied pixel-to-millimetre factor. This is an implemented OpenCV triage workflow; it is not a trained YOLO detector, calibrated probability estimate or structural diagnosis.

### 5.2 Digital twin, telemetry and preliminary screening

The digital-twin engine generates frame nodes and members from floors, bays, spacing and storey height. It produces deterministic synthetic temperature, wind, strain and tilt series. Its structural screening functions calculate tributary gravity, axial stress, simplified beam stress, wind pressure, hydrostatic pressure and a utilisation indicator. These outputs are transparent first-pass indicators and require qualified engineering review.

### 5.3 Reporting, cost and integration boundary

The specialised pages provide damage analysis, cost estimation, history and report-generation workflows. The worker dispatcher checks the availability of COLMAP, OpenSees and OpenFOAM executables. A missing executable produces `BLOCKED`, rather than a simulated engineering result. This boundary is an important mid-term safety property.

## 6. User Interface and Visualisation

The root command centre provides Portfolio, Command center, Twin studio, Capture and reconstruction, Asset health, IoT Telemetry and CCTV, and Integration views. The specialised `pages/` directory adds tutorial, virtual practical, GPS, AI inspection, damage analysis, 3D building, IoT, cost estimation, materials, history, reports and settings views.

The interface is the communication layer for inspection evidence and assumptions. Visual displays can make a workflow easier to understand, but they do not establish measurement accuracy, live data quality or code-compliant structural performance on their own.

## 7. Technology Stack

| Layer | Technology/tool | Current purpose |
| --- | --- | --- |
| Core language | Python | Application logic, data handling and prototype orchestration. |
| Frontend | Streamlit | Dashboard and inspection workflow interface. |
| Image processing | OpenCV and Pillow | Rule-based image processing and annotation. |
| Data processing | NumPy and Pandas | Geometry, synthetic telemetry and tabular calculations. |
| Visualisation | Plotly, Three.js and Folium | Parametric/3D and map-oriented visual displays. |
| Data contracts | Pydantic | Validation for asset, capture, telemetry and analysis requests. |
| Local reference storage | SQLite | Prototype storage for assets, captures, telemetry and jobs. |
| Future worker targets | COLMAP, OpenSees and OpenFOAM | Readiness-checked reconstruction and engineering analysis services. |

## 8. Challenges and Resolutions

| Challenge | Engineering response | Status |
| --- | --- | --- |
| Risk of unsupported AI claims | Documentation and evidence matrix distinguish OpenCV triage from trained YOLO inference. | **Addressed** |
| Risk of unsupported solver claims | Dispatcher returns explicit `READY`/`BLOCKED` state and does not create a result when a solver is unavailable. | **Addressed** |
| Measurement uncertainty | Interface exposes a user-supplied scale factor and documentation labels dimensions approximate. | **Partially addressed** |
| Fragmented prototype modules | Root command centre and specialised pages coexist; navigation consolidation is still needed. | **In progress** |
| Demonstration versus field data | Synthetic telemetry is explicitly labelled synthetic and requires replacement by quality-controlled field data. | **In progress** |

## 9. Remaining Work and Deployment Roadmap

The next phase should complete a reviewable evidence loop rather than add unsupported features:

1. Consolidate the active user journey and add automated tests for contracts and screening calculations.
2. Define calibrated capture procedures and collect a consented, labelled image dataset.
3. Establish model/version tracking and evaluate any detector with held-out data, false-negative analysis and calibration metrics.
4. Connect approved telemetry hardware through authenticated ingestion, timestamp and quality checks, and durable storage.
5. Integrate external reconstruction/solver workers only with versioned inputs, logs, output artifacts and engineer review.
6. Add authentication, role-based approvals, retention policy, audit records and report-version controls before a field pilot.

## 10. Interim Conclusion

At the mid-term checkpoint, ConstructVision AI has progressed beyond concept definition into a coherent prototype architecture. The team has established an evidence-first workflow, implemented transparent image-triage and screening components, created visual and reporting interfaces, and introduced data/worker boundaries that avoid fabricated engineering results. The remaining work is primarily validation and controlled integration: calibrated field data, test evidence, secure persistence, qualified review and solver-backed analysis. These steps are required before the prototype can be represented as a decision-grade infrastructure-inspection system.

## References

1. A. A. A. Elhariri et al., “Computer vision framework for crack detection of civil infrastructure: A review,” *Journal of Building Engineering*, vol. 67, 2023, doi: 10.1016/j.jobe.2022.105979.
2. R. Sacks et al., “Construction with digital twin information systems,” *Data-Centric Engineering*, vol. 1, e14, 2020, doi: 10.1017/dce.2020.16.
3. C. R. Farrar and K. Worden, *Structural Health Monitoring: A Machine Learning Perspective*. Wiley, 2012.
4. A. Chopra, *Dynamics of Structures: Theory and Applications to Earthquake Engineering*, 5th ed. Pearson, 2017.

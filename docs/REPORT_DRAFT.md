# ConstructVision AI — full project report draft

> Submission note: replace every bracketed placeholder with verified institutional and project-specific information. Add only measured model metrics, screenshots, references and test results that can be evidenced.

## Title page

**ConstructVision AI: an evidence-first digital-twin workflow for construction inspection**  
Project report submitted by **[Name(s)]**  
Programme / Department: **[Programme]**  
Institution: **[Institution]**  
Mentor / Supervisor: **[Name]**  
Submission date: **[Date]**

## Certificate, declaration and acknowledgements

Insert institution-approved certificate language, a signed originality declaration, contributor roles, acknowledgement of mentors/data providers, and the licence status of all third-party assets and models.

## Abstract

See [ABSTRACT.md](ABSTRACT.md). Include 200–300 words in the final submitted report and retain the keyword list.

## Table of contents

1. Introduction  
2. Problem statement and objectives  
3. Literature and technology context  
4. Design philosophy and scope  
5. Requirements and methodology  
6. System architecture and implementation  
7. User experience and portfolio presentation  
8. Testing and evaluation  
9. Ethics, safety and limitations  
10. Deployment and operations  
11. Results, conclusion and future work  
12. References and appendices

---

## Chapter 1 — Introduction

Construction inspection information is often dispersed across photographs, site records, spreadsheets, material specifications and verbal communication. This slows review, weakens traceability and makes it difficult to understand whether an observed condition is merely visual, measured, modelled or approved. ConstructVision AI is a project foundation that brings these artefacts into an explicit digital-twin workflow.

The project presents two connected experiences. First, a portfolio landing page explains the problem, system philosophy, architecture and roadmap to reviewers, recruiters and collaborators. Second, a product workspace demonstrates an asset command centre, parametric 3D frame, capture intake, health view and solver-integration status. A FastAPI service exposes the contracts underpinning the workflow.

### 1.1 Motivation

The intended value is not to replace engineers. It is to make evidence easier to collect, interpret, locate and review. The project is especially relevant where inspection teams need a clear boundary between preliminary AI-assisted triage and decision-grade structural analysis.

### 1.2 Project scope

In scope are: asset registration; capture-package metadata; telemetry ingestion contracts; preliminary parametric visualisation and screening; a portfolio UI; documentation; and deployment planning. Out of scope for the current prototype are metric photogrammetry output, validated finite-element results, CFD results, certified defect diagnosis and production device integration.

## Chapter 2 — Problem statement and objectives

### 2.1 Problem statement

Site observations frequently lack a unified record of location, source, model revision, uncertainty and subsequent action. A rich visual dashboard can be misleading if it obscures these gaps. The problem addressed is how to organise inspection evidence and engineering workflows in a transparent, extensible system.

### 2.2 Objectives

1. Create a premium, navigable portfolio interface that communicates the project clearly.
2. Establish API contracts for assets, captures, telemetry and analysis jobs.
3. Demonstrate a parametric 3D structural context and preliminary load screening.
4. Preserve an explicit audit boundary between visualisation, screening and validated engineering computation.
5. Produce a report, deployment plan and repository structure suitable for continued full-stack development.

### 2.3 Success criteria

- A reviewer can understand the value proposition and workflow without navigating source code.
- Local API endpoints validate well-formed input and return clear service states.
- The UI shows solver unavailability rather than inventing an engineering outcome.
- Documentation states limitations, responsibilities and production requirements clearly.

## Chapter 3 — Literature and technology context

Digital twins combine a representation of a physical asset with evidence and operational context. In construction, the term should not be used merely for a 3D model: a defensible implementation requires versioning, provenance, uncertainty and a review process. Computer vision can prioritise images for human review, but its accuracy varies by data quality, lighting, camera position, material condition and training distribution. Structural health monitoring similarly needs calibrated sensors, unit-aware records, quality flags and domain interpretation.

The prototype uses Streamlit for rapid product exploration, Plotly for parametric 3D visualisation, FastAPI/Pydantic for typed service boundaries, and SQLite for a local reference store. These technologies are appropriate for a demonstration; production scale requires a separately deployed web client, secure persistence and isolated solver workloads.

## Chapter 4 — Design philosophy and scope

### 4.1 Evidence before spectacle

High-fidelity visuals are useful for orientation but cannot establish measurement accuracy. Three oblique photographs are not a calibrated, metric reconstruction. An animated wind field is not a CFD result. This principle informs both UI language and API responses.

### 4.2 Human accountability

AI is used as an assistive mechanism for triage and documentation. It cannot issue a structural safety certificate. A qualified and licensed engineer must review design-grade interpretations and sign off where required by law or policy.

### 4.3 Interoperability and provenance

Asset models, captures, telemetry and solver results should be separately versioned and linked. The preferred future formats are API contracts plus glTF/3D Tiles for visual geometry and immutable object-storage artefacts for evidence.

## Chapter 5 — Requirements and methodology

### 5.1 Functional requirements

| ID | Requirement | Prototype status |
| --- | --- | --- |
| FR-01 | Register an asset with a name and location | Implemented via API |
| FR-02 | Register a capture package with calibration metadata | Implemented via API contract |
| FR-03 | Ingest timestamped, unit-aware telemetry samples | Implemented via API contract |
| FR-04 | Request reconstruction/FEA/CFD/flood analysis | Implemented; dependent on worker availability |
| FR-05 | Visualise an editable structural frame | Implemented as parametric Plotly view |
| FR-06 | Present project narrative and roadmap | Implemented as portfolio landing experience |

### 5.2 Non-functional requirements

The platform should provide typed validation, clear error states, UTC timestamps, immutable-source references, responsive presentation, auditable deployment configuration and security controls before public data is processed.

### 5.3 Method

The development method is iterative: define contracts before automation; build a visual narrative around verified capabilities; exercise services locally; document the boundary of each result; then harden deployment and add workers only after repeatable test cases exist.

## Chapter 6 — System architecture and implementation

### 6.1 Architecture

```text
Portfolio / product UI
        │
FastAPI contracts ──> local SQLite reference store
        │                     │
Capture metadata / telemetry  └──> production: PostgreSQL + TimescaleDB
        │
Analysis-job queue ──> isolated COLMAP / OpenSees / OpenFOAM workers
                              │
                         immutable result artefacts
```

### 6.2 API layer

`api/main.py` exposes a health endpoint plus endpoints for assets, capture packages, telemetry batches and analysis jobs. Pydantic models restrict expected fields; for example, a capture package requires an object-storage or file URI and telemetry records contain timestamps, unit, quality and sensor identity.

### 6.3 Local persistence

`platform_core/store.py` implements SQLite storage for local development. It creates asset, capture, telemetry and analysis-job tables. This is explicitly a reference implementation and not a multi-user production database.

### 6.4 3D and preliminary analysis

`modules/digital_twin/engine.py` generates nodes and members for a regular structural frame, visualised through Plotly. It calculates simplified gravity, flexural, wind-pressure and hydrostatic indicators. The result is labelled as screening only. Its inputs and assumptions must not be used for design without validated models and qualified review.

### 6.5 Worker boundary

The dispatcher checks for COLMAP, OpenSees and OpenFOAM executables. When unavailable, jobs are reported as blocked. This is intentional: a service must not convert an unavailable solver into a cosmetic or fabricated result.

## Chapter 7 — User experience and portfolio presentation

The landing page is designed as a case-study narrative. It includes navigation for platform proposition, workflow, architecture, philosophy, roadmap and documentation. The visual language uses a dark technical palette, restrained grid texture, high-contrast typography and card-based information hierarchy. The public page gives a non-technical reviewer a clear path into the deeper product workspace.

The workspace navigation separates Portfolio, Command Center, Twin Studio, Capture & Reconstruction, Asset Health and Integration. This makes the primary story visible without hiding implementation evidence.

## Chapter 8 — Testing and evaluation

### 8.1 Current validation evidence

- Python compilation was run for the API, platform core, workers, modules and application entry point.
- The FastAPI service was started locally and `GET /health` returned an `ok` response.
- Solver-readiness checks reported COLMAP, OpenSees and OpenFOAM as unavailable in the local environment.

### 8.2 Required final evaluation

Add evidence rather than estimates for each item below.

| Area | Measure | Evidence to include |
| --- | --- | --- |
| API | endpoint status, validation failures, response time | automated test log and screenshots |
| UI | task completion and responsive layout | usability notes and viewport screenshots |
| Vision | precision, recall, mAP, false-negative analysis | held-out dataset and reproducible evaluation |
| Reconstruction | scale error, coverage, alignment error | calibrated capture set and QA report |
| Solver | benchmark agreement and mesh sensitivity | validated reference problem, logs, artifacts |
| Security | dependency, secrets and access-control checks | CI reports and review record |

### 8.3 Limitations of current results

No model-accuracy, inference-speed, reconstruction-accuracy or structural-performance claims should be published unless they are measured with documented data and methodology. Placeholder dashboard values are demonstrative only.

## Chapter 9 — Ethics, safety and limitations

Images may contain identifiable workers, private properties or sensitive site context; collection must follow consent, retention and access policies. AI outputs can be biased by data coverage and should be reviewed by trained personnel. Engineering results must retain assumptions and be signed off through the appropriate professional process. The system must never represent a blocked or preliminary process as an approved result.

## Chapter 10 — Deployment and operations

### 10.1 Target deployment

- API service: containerised FastAPI behind a TLS reverse proxy.
- Client: separate dashboard/web-client deployment with a public domain.
- Data: managed PostgreSQL + TimescaleDB, object storage and encrypted backups.
- Identity: OAuth/OIDC, RBAC, service credentials and a secrets manager.
- Jobs: durable queue with isolated worker containers and artifact retention.
- Observability: structured logs, health/readiness endpoints, metrics and alerting.

### 10.2 GitHub delivery checklist

1. Create or select the target GitHub repository and confirm ownership.
2. Add `.env.example`, licence, contribution guidance and security policy.
3. Add tests and GitHub Actions for linting, API tests and container builds.
4. Configure deployment secrets only in GitHub or the hosting platform—never commit them.
5. Deploy API and client, attach a domain, test HTTPS and document the final URLs.

## Chapter 11 — Results, conclusion and future work

ConstructVision AI demonstrates a coherent starting point for an evidence-first construction intelligence platform. Its principal contribution is the explicit combination of project narrative, typed data contracts, visual context and responsible engineering boundaries. The next milestone is not cosmetic complexity; it is production hardening and repeatable validation.

Future work includes role-based access control, real object storage, PostgreSQL/TimescaleDB, MQTT ingestion, labelled defect datasets, calibrated photogrammetry, BIM/IFC import, browser-native 3D viewing, durable jobs, tested solver containers and engineer-approved scenario templates.

## Chapter 12 — References

Use a consistent citation style specified by the institution. Include primary sources for standards, framework documentation, research papers, datasets and model licences. Do not cite generated prose as a technical source.

Suggested reference categories:

- National or regional structural design and inspection standards relevant to the project.
- Official FastAPI, Pydantic, Streamlit and Plotly documentation.
- Peer-reviewed work on construction defect detection, photogrammetry and structural health monitoring.
- Official COLMAP, OpenSees and OpenFOAM documentation.

## Appendices

### Appendix A — API endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/health` | Service liveness response |
| POST | `/v1/assets` | Create asset record |
| POST | `/v1/captures` | Register capture package |
| POST | `/v1/telemetry:ingest` | Submit telemetry batch |
| POST | `/v1/analysis-jobs` | Queue analysis request |
| GET | `/v1/analysis-jobs/{job_id}` | Read job record |

### Appendix B — Local run instructions

```powershell
.\.venv\Scripts\python.exe -m uvicorn api.main:app --host 127.0.0.1 --port 8000
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

### Appendix C — Suggested screenshots

1. Portfolio landing page hero and architecture section.
2. Command center and parametric 3D frame.
3. Capture/reconstruction workflow and guidance.
4. API Swagger endpoint list and health response.
5. Solver blocked state, showing honest capability signalling.

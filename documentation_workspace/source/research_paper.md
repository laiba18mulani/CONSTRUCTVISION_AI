# ConstructVision AI: An Evidence-First Digital-Twin Architecture for AI-Assisted Civil Infrastructure Inspection

**Ritika M. Bhumkar** (ritikambhumkar@gmail.com) and **Laiba Z. Mulani** (laiba.mulani.ces.34@gmail.com)  
Diploma Third Year Civil Engineering  

**Industry Guide:** Mr. Akash S. Chatake, M.TECH - AIML - BITS PILANI  
**College Guide:** Ms. Swati P. Maniyal, M.TECH - Structural Engineering  

**Chatake Innoworks Private Limited** | **MindForgeAI Internship Division**  
www.chatakeinnoworks.com | https://mindforgeai.co.in

## Abstract

Civil infrastructure inspection remains fragmented across photographs, paper observations, spreadsheets, sensor streams and engineer judgement. ConstructVision AI is an evidence-first digital-twin prototype that explores a unified command centre for structural context, inspection triage, telemetry, preliminary mechanics and repair costing. The implemented system uses Streamlit for the interaction layer, OpenCV for rule-based image analysis, Three.js and Plotly for parametric three-dimensional visualisation, Pydantic contracts for typed asset and telemetry records, and a worker-readiness boundary for future reconstruction, finite-element, computational-fluid-dynamics and flood jobs. The prototype converts image contours into approximate crack dimensions through an explicit pixel-to-millimetre calibration, classifies severity with transparent thresholds, and computes screening indicators for gravity, flexure, wind pressure and hydrostatic pressure. It also provides cost estimation from area, material coverage, urgency, labour, scaffolding and GST. The contribution is therefore architectural and methodological: it demonstrates how visual outputs, assumptions, uncertainty and human review can be kept connected rather than allowing a compelling 3D view to be mistaken for certified engineering evidence. YOLOv8-based detection, ESG carbon forecasting and four-dimensional seismic response are specified as validated extension paths, not represented as capabilities already measured in the current checkout. The paper proposes a mathematical integration layer for these extensions, including detection loss, seismic response, energy conversion and embodied-carbon accounting. A rigorous evaluation protocol is defined around precision, recall, mAP, calibration error, latency, reconstruction error, forecast error and engineer agreement. The resulting system is a responsible foundation for future deployment in civil infrastructure inspection.

**Keywords:** civil infrastructure inspection; digital twin; computer vision; structural health monitoring; Streamlit; seismic simulation; embodied carbon; evidence provenance.

## 1. Introduction

Inspection teams must combine visual observations, component identity, location, condition, environmental context and recommended action. In practice, these facts are often stored in different artefacts. A defect can be photographed on site, described in a log, measured later and finally transferred to a report without a stable link to the building element or the model revision used for interpretation. Manual inspection remains essential, but it is time-intensive, difficult to standardise and vulnerable to inconsistent documentation.

ConstructVision AI addresses this workflow problem through a browser-based command centre. Its current implementation is a prototype, not a safety-certification system. The project links a parameterised structural frame, inspection images, simulated telemetry, preliminary mechanics, cost estimation and future analysis jobs. Its central design principle is evidence before spectacle: a parametric model is not a calibrated reconstruction; a visual animation is not a validated solver result; and an AI flag is not a professional sign-off.

### 1.1 Research gap

Prior research has separately advanced computer-vision defect detection, structural-health monitoring, building information modelling and digital twins. The unresolved engineering gap is operational integration under uncertainty. A useful inspection twin must preserve source imagery, calibration, component identity, model revision, sensor quality, analysis status and reviewer responsibility in one auditable chain. The present work contributes a reference architecture and transparent screening mathematics for this integration.

### 1.2 Contributions

1. An evidence-first architecture connecting capture, inspection, spatial context, telemetry, screening and reporting.
2. A traceable implementation analysis grounded in the current Python and Streamlit codebase.
3. Mathematical formulations for the implemented screening calculations and proposed YOLOv8, seismic and carbon extensions.
4. An evaluation protocol that separates measured performance from simulated demonstration values.
5. A governance boundary that prevents unavailable external solvers from being represented as completed engineering analyses.

## 2. Literature review

Computer-vision crack detection research has progressed from thresholding and edge operators to supervised detection, segmentation and multimodal assessment. Reviews identify acquisition quality, lighting, material texture, scale and dataset bias as persistent limitations [1]-[4]. One-stage detectors are attractive for field triage because they provide low-latency predictions, but a deployment requires a labelled dataset, train/validation/test partitioning, class definitions, calibration strategy and false-negative analysis.

Digital twins in construction are more than three-dimensional models. They combine a physical asset, a digital representation, data exchange and a lifecycle process. Reviews emphasise interoperability, synchronisation, data quality, semantics, cybersecurity and the difficulty of maintaining a reliable relationship between model and asset [5]-[8]. Structural-health monitoring adds time-series sensing and damage-sensitive features, but sensor drift, environmental variability and missing data must be handled explicitly [9].

Seismic response analysis is normally conducted with validated structural models, ground-motion records and code-defined combinations. A browser animation can communicate a scenario but cannot replace modal analysis or nonlinear time-history analysis. Similarly, carbon accounting requires defined system boundaries, activity data, emission factors and reporting periods; a dashboard label alone is not an ESG inventory [10]-[12].

The research gap is therefore not the absence of individual algorithms. It is the absence of a transparent bridge from an observation to a reviewable engineering action. ConstructVision's current prototype makes that bridge explicit, while leaving high-stakes algorithms behind versioned validation gates.

## 3. Methodology

### 3.1 Current inspection pipeline

`pages/5_🔬_AI_Inspection.py` accepts a camera frame, uploaded field image, or synthetic demonstration target. The active rule-based pipeline is:

1. Convert the RGB input to grayscale and HSV colour spaces.
2. Optionally suppress probable sky/glare and vegetation regions with HSV masks.
3. Apply a Gaussian blur with a $5\times5$ kernel.
4. Apply Canny edge detection with the user-selected sensitivity $k$ and upper threshold $2k$; the default is $k=45$.
5. Join nearby edge fragments with a $3\times3$ morphological closing operation.
6. Extract external contours and discard a contour whose closed perimeter $P$ is below the user-selected minimum threshold $P_{min}$; the default is 30 px.
7. Retain elongated or sparse contours using aspect ratio and extent, then estimate length, width and area with the user-supplied scale $s$ in mm/px:

$$L_{px}=P/2, \qquad W_{px}=A_c/L_{px},$$

$$L_{mm}=sL_{px}, \qquad W_{mm}=\operatorname{clip}(sW_{px},0.08,6.50).$$

8. Assign the implemented interface severity:

$$C(W_{mm})=
\begin{cases}
\text{CRITICAL (Grade III)},&W_{mm}>0.30\\
\text{MODERATE (Grade II)},&0.10\leq W_{mm}\leq0.30\\
\text{NOMINAL (Grade I)},&W_{mm}<0.10.
\end{cases}$$

This is an OpenCV rule-based triage workflow, not YOLO inference or calibrated defect probability. Any confidence figures shown elsewhere in the prototype are interface/demo values unless linked to a trained model, an evaluation set and a calibration analysis.

### 3.2 Proposed YOLOv8 extension

The repository contains settings labels for YOLOv8-X/N and a zero-byte placeholder named `models/yolov11.pt`; it does not contain a usable model checkpoint, YOLO inference call or dataset loader wired into the active inspection page. The proposed production path is an anchor-free, decoupled-head detector with a backbone-neck feature pyramid and defect classes such as crack, spalling, exposed reinforcement, honeycombing, leakage and corrosion.

For a predicted box $\hat b=(\hat x,\hat y,\hat w,\hat h)$ and ground-truth box $b$, a composite objective can be written as:

$$\mathcal L=\lambda_{box}\mathcal L_{CIoU}+\lambda_{cls}\mathcal L_{BCE}+\lambda_{dfl}\mathcal L_{DFL},$$

where

$$\mathcal L_{CIoU}=1-IoU+\frac{\rho^2(\hat c,c)}{d^2}+\alpha v,$$

and $v$ measures aspect-ratio inconsistency. For class imbalance, focal weighting may be added:

$$\mathcal L_{focal}=-\alpha_t(1-p_t)^\gamma\log(p_t).$$

These equations describe a proposed training specification; they are not evidence that this checkout trained YOLOv8.

### 3.3 Digital-twin geometry and telemetry

`modules/digital_twin/engine.py` defines `TwinInputs` containing floors, bays, bay spacing, storey height, concrete strength, member dimensions, wind speed, rainfall, flood depth and live load. Frame nodes are generated by:

$$\mathbf n_{xyz}=(x\,b,\;y\,b,\;z\,h_s),$$

for integer grid indices. Members connect vertical nodes as columns and adjacent same-level nodes as beams. The deterministic telemetry generator samples temperature, wind, strain and tilt. With a random generator seed, it computes:

$$T_t=25+6\sin(\theta_t)+\epsilon_T,$$

$$V_t=\max\{0,8+5\sin(\phi_t)+\epsilon_V\},$$

$$\varepsilon_t=165+1.2T_t+2.3V_t+\epsilon_\varepsilon,$$

$$\vartheta_t=0.15+0.012V_t+\epsilon_\vartheta.$$

These values are synthetic telemetry for interface demonstration.

### 3.4 Preliminary structural screening

For an interior lower-storey column, tributary area, gravity action, column area and axial stress are:

$$A_t=b^2,$$

$$P=(6.0+q_L)A_t n_f,$$

$$A_c=(d_c/1000)^2,$$

$$\sigma_a=P/(1000A_c).$$

The code uses $0.40f'_c$ as a screening capacity indicator. The simplified beam line load and moment are:

$$w=(6.0+q_L)b,\qquad M=\frac{wb^2}{8},$$

with section-modulus indicator $Z=(d_b/1000)^3/6$ and $\sigma_f=M/(1000Z)$. Wind and hydrostatic pressures are:

$$q_w=0.613V^2/1000\;\text{kPa},\qquad p_h=9.81h_f\;\text{kPa}.$$

The utilisation index is:

$$U=\max\left(\frac{\sigma_a}{0.40f'_c},\frac{\sigma_f}{0.60f'_c}\right).$$

The code returns `Review required` when $U\geq0.8$. These are transparent screening indicators, not code-compliant design checks.

### 3.5 Proposed 4D seismic simulation

The current UI includes a `Seismic Oscillation` selector, but the checkout has no seismic ground-motion record or dynamic solver. A future validated module can define a base-excited multi-degree-of-freedom model:

$$\mathbf M\ddot{\mathbf u}+\mathbf C\dot{\mathbf u}+\mathbf K\mathbf u=-\mathbf M\mathbf r\ddot u_g(t),$$

where $\mathbf u$ is relative displacement and $\ddot u_g(t)$ is ground acceleration. A modal approximation is:

$$u(z,t)=\sum_{r=1}^{m}\phi_r(z)q_r(t),$$

with modal coordinates satisfying:

$$\ddot q_r+2\zeta_r\omega_r\dot q_r+\omega_r^2q_r=-\Gamma_r\ddot u_g(t).$$

For a visualised inter-storey drift:

$$\Delta_i(t)=u_i(t)-u_{i-1}(t),\qquad \,\theta_i(t)=\frac{\Delta_i(t)}{h_i}.$$

The simulation should use recorded or code-compatible motions, validated mass/stiffness matrices, time-step convergence and engineer review. It must not be presented as implemented merely because the UI animates sway.

### 3.6 Proposed ESG carbon forecasting

No carbon calculation is present in the source. A future activity-based inventory can compute:

$$E_{CO_2e}=\sum_{j=1}^{N}A_j\,EF_j\,CF_j,$$

where $A_j$ is activity data, $EF_j$ an emission factor and $CF_j$ a conversion or global-warming-potential factor. A time-series forecast can model monthly emissions as:

$$\hat E_{t+h}=f(E_{1:t},\mathbf x_{1:t+h};\Theta),$$

with uncertainty intervals $[\hat E_{t+h}^{L},\hat E_{t+h}^{U}]$. The system should retain source, factor version, boundary, unit and reporting period for every term.

## 4. Implementation and system architecture

The platform has two overlapping Streamlit interface layers: a newer root command centre in `app.py` and 13 specialised prototype pages in `pages/`. The specialised pages are:

1. Home/command centre and project portfolio.
2. Tutorial and training workflow.
3. Virtual practical laboratory.
4. GPS location and drone-flight GIS.
5. AI inspection and crack triage.
6. Damage analysis and repair protocol.
7. Structural digital-twin and 3D building viewer.
8. IoT/sensor-node visualisation.
9. Cost estimation and bill generation.
10. Materials knowledge library.
11. Historical inspection records.
12. Report generation.
13. Settings, calibration and governance.

The root `app.py` exposes Portfolio, Command center, Twin studio, Capture & reconstruction, Asset health, IoT Telemetry & CCTV, and Integration views. `platform_core/contracts.py` defines typed asset, capture, telemetry and analysis-job models, while `platform_core/store.py` provides a local SQLite reference store for assets, captures, telemetry and analysis jobs. `workers/dispatcher.py` checks whether COLMAP, OpenSees and OpenFOAM executables are installed and returns `READY` or `BLOCKED`; this is a valuable safety property because unavailable analyses are not fabricated.

## 5. Results and discussion

### 5.1 Verified implementation results

The code supports a runnable interface, deterministic demo telemetry, parametric frame geometry, transparent screening formulas, rule-based image contour annotation, repair-cost calculation, report-history views, typed contracts and a local SQLite reference store. Reconstruction, FEA, CFD and production-grade IoT integration remain future integrations.

### 5.2 Simulated demonstration metrics

The following values are planning targets for a future evaluation harness, not measured results from this checkout: detector mAP@0.5 $\geq0.85$; defect recall $\geq0.90$; calibrated confidence error $\leq0.05$; single-image inference latency $\leq200$ ms on an edge GPU; telemetry-to-alert latency $\leq2$ s; crack-width mean absolute error $\leq0.5$ mm after calibrated capture; and carbon forecast MAPE $\leq15\%$. They must be replaced with dataset-backed measurements before journal submission.

### 5.3 Discussion

The most defensible current contribution is traceability. The prototype makes assumptions visible, uses explicit formulas, exposes the calibration ratio, and keeps solver unavailability visible. Its principal weakness is that the strongest requested claims - YOLOv8 accuracy, seismic response fidelity and ESG forecasting quality - cannot yet be supported by executable evidence. The research programme should therefore prioritise labelled data, calibration, versioned model artefacts, validation cases, uncertainty reporting and professional review before adding visual complexity.

## 6. Conclusion and future scope

ConstructVision AI demonstrates how an infrastructure-inspection interface can connect images, geometry, telemetry, mechanics, costing and workflow governance. Its evidence-first architecture is suitable as a foundation for a validated digital twin, but the present implementation is a prototype and must not issue safety certificates or design approvals. Future work should integrate a trained detector, calibrated photogrammetry or BIM/IFC input, time-synchronised sensor streams, validated OpenSees/FEA workflows, seismic response histories, activity-based carbon accounting, role-based access control, immutable evidence storage and independent civil-engineering review.

## References

[1] A. A. A. Elhariri et al., “Computer vision framework for crack detection of civil infrastructure - A review,” *Journal of Building Engineering*, vol. 67, 2023, doi: 10.1016/j.jobe.2022.105979.

[2] Y. Fujita et al., “A practical method for crack detection from noisy concrete surfaces,” *Machine Vision and Applications*, vol. 23, pp. 83-94, 2012.

[3] S. Dorafshan, R. J. Thomas, and M. Maguire, “Comparison of deep convolutional neural networks and edge detectors for image-based crack detection in concrete,” *Construction and Building Materials*, vol. 186, pp. 1031-1045, 2018.

[4] H. M. Laofor and A. H. A. Alani, “What's cracking? A review and analysis of deep learning methods for structural crack segmentation, detection and quantification,” arXiv:2202.03714, 2022.

[5] R. Sacks et al., “Construction with digital twin information systems,” *Data-Centric Engineering*, vol. 1, e14, 2020, doi: 10.1017/dce.2020.16.

[6] A. Boje et al., “Towards a semantic construction digital twin: Directions for future research,” *Automation in Construction*, vol. 114, 2020, doi: 10.1016/j.autcon.2020.103179.

[7] Y. Liu et al., “Transforming data into decision making: A spotlight review of construction digital twin,” *Buildings*, vol. 11, no. 12, 2021, doi: 10.3390/buildings11120598.

[8] M. Opoku et al., “Digital twin and its applications in the construction industry: A state-of-art systematic review,” *Digital Twin*, vol. 2, 2024, doi: 10.12688/digitaltwin.17664.3.

[9] C. R. Farrar and K. Worden, *Structural Health Monitoring: A Machine Learning Perspective*. Wiley, 2012.

[10] S. G. A. Flannery et al., “A comprehensive review of digital twin implementation in construction: Current trends and future directions,” *Journal of Asian Architecture and Building Engineering*, 2025, doi: 10.1080/13467581.2025.2517242.

[11] GHG Protocol, *A Corporate Accounting and Reporting Standard*, revised ed., World Resources Institute and World Business Council for Sustainable Development, 2004.

[12] ISO 14064-1:2018, *Greenhouse gases - Part 1: Specification with guidance at the organization level for quantification and reporting of greenhouse gas emissions and removals*, ISO, 2018.

[13] K. He et al., “Deep residual learning for image recognition,” in *Proc. IEEE CVPR*, 2016, pp. 770-778.

[14] J. Redmon et al., “You only look once: Unified, real-time object detection,” in *Proc. IEEE CVPR*, 2016, pp. 779-788.

[15] G. Jocher, A. Chaurasia, and J. Qiu, *Ultralytics YOLO*, software and documentation, 2023. [Online]. Available: https://github.com/ultralytics/ultralytics

[16] FEMA P-1050, *NEHRP Recommended Seismic Provisions for New Buildings and Other Structures*, Federal Emergency Management Agency, 2020.

[17] A. Chopra, *Dynamics of Structures: Theory and Applications to Earthquake Engineering*, 5th ed. Pearson, 2017.

[18] M. P. Groover, *Automation, Production Systems, and Computer-Integrated Manufacturing*, 4th ed. Pearson, 2015.

## Appendix A. Reproducibility and validity protocol

This paper describes a prototype implementation and a validation agenda. A future empirical version must publish a reproducibility package containing: the source revision; dependency lockfile; operating-system and hardware record; configuration values; de-identified dataset manifest; annotation guide; train/validation/test split rule; random seeds; trained-model hash; evaluation script; and complete tables for per-class errors. Results from synthetic telemetry must be labelled synthetic and must not be mixed with field measurements in aggregate metrics.

For image measurement, the capture protocol should specify camera-to-surface distance, viewing angle, lighting condition, scale target dimensions, image resolution and surface type. The reference measurement method should be stated before testing. Measurement performance should report mean absolute error, root-mean-square error, bias and a confidence interval by crack-width band.

For a structural solver workflow, retain the geometry/model revision, material definitions, boundary conditions, load cases, ground-motion record where applicable, solver version, time step, convergence settings, output files and engineer review. A visual animation is excluded from structural validation unless it is generated from the stored solver result.

## Appendix B. Claim taxonomy for publications and demonstrations

| Status | Meaning | Example wording |
| --- | --- | --- |
| Implemented | Executable behaviour directly evidenced in this checkout. | “The prototype generates a parametric frame and preliminary screening indicator.” |
| Demonstration | Synthetic data or illustrative workflow used to explain the interface. | “The dashboard displays deterministic synthetic telemetry for demonstration.” |
| Readiness boundary | A request is validated or a dependency is checked, but no external computation has been completed. | “The dispatcher reports whether an OpenSees worker is available.” |
| Proposed | Architecture, equation or requirement not implemented and tested in this checkout. | “A future detector may be evaluated using mAP and calibration error.” |
| Validated | A result independently supported by a documented method and dataset. | Use only after the reproducibility package and appropriate review are available. |

This taxonomy provides a simple safeguard for posters, oral examinations, reports and product demonstrations. It prevents target metrics from appearing to be results and distinguishes a digital representation from an engineering-certified model.

## Appendix C. Deployment research questions

1. Does evidence linkage reduce the time required for an engineer to locate the source and assumptions behind an inspection finding?
2. Under which surface, lighting and capture conditions does calibrated image measurement remain within an agreed error tolerance?
3. Does a model trained on one project, material or camera generalise to another without unacceptable false negatives?
4. Which telemetry quality rules minimise false alerts while preserving timely escalation of abnormal readings?
5. Can reviewers consistently distinguish a preliminary screening result from a code-based structural assessment after using the interface?
6. What governance, privacy and retention controls are required for a real owner/operator deployment?

Answering these questions with a representative field study would transform the present architectural contribution into an evidence-backed deployment study.

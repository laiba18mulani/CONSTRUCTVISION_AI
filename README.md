## ConstructVision AI — digital twin and project portfolio

ConstructVision is an evidence-first built-environment intelligence project. The default Streamlit experience is a portfolio landing page that introduces the project, philosophy, workflow, architecture and roadmap; the same app also contains the operational twin workspace.

The API-first platform foundation lives in `api/`, `platform_core/`, and `workers/`. The existing `pages/` directory contains the evolving prototype modules.

## Run locally

Run the platform API:

```powershell
.\.venv\Scripts\uvicorn.exe api.main:app --reload --port 8000
```

Open `http://127.0.0.1:8000/docs` for the API contract. See `docs/PRODUCT_REBUILD.md` for the system design and delivery sequence.

Run the portfolio and workspace:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Open `http://127.0.0.1:8501`.

## Documentation

- [Project abstract](docs/ABSTRACT.md)
- [Full project report draft](docs/REPORT_DRAFT.md)
- [Product rebuild architecture](docs/PRODUCT_REBUILD.md)

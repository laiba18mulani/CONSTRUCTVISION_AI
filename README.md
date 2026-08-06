## ConstructVision Digital Twin

The legacy Streamlit prototype is retained for reference only. The product rebuild is API-first and lives in `api/`, `platform_core/`, and `workers/`.

Run the platform API:

```powershell
.\.venv\Scripts\uvicorn.exe api.main:app --reload --port 8000
```

Open `http://127.0.0.1:8000/docs` for the API contract. See `docs/PRODUCT_REBUILD.md` for the system design and delivery sequence.

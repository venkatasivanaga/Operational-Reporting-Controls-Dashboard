# Backend (FastAPI)

## Conda environment
This repo uses a conda env named: orcd

Install dependencies:
- conda run -n orcd python -m pip install -r backend/requirements.txt

Run API:
- conda run -n orcd uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000

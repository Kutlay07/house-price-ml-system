FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY models/ models/
COPY tests/ tests/
COPY api/ api/

CMD ["uvicorn", "api.main:app", "--host",  "0.0.0.0", "--port", "8000"]

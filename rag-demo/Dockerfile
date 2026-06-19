FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY rag-demo/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY content /app/content
COPY rag-demo /app/rag-demo

WORKDIR /app/rag-demo
RUN python ingestion/build_index.py

EXPOSE 8080

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]

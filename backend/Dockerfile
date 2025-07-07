FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /workspace/backend

RUN python -m venv /workspace/backend/.venv
ENV PATH="/workspace/backend/.venv/bin:$PATH"

COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir debugpy

COPY backend/app /workspace/backend/app
COPY backend/start.sh /workspace/backend/start.sh

RUN chmod +x /workspace/backend/start.sh

ENV PYTHONPATH=/workspace/backend \
    PYTHONUNBUFFERED=1

CMD ["/workspace/backend/start.sh"]

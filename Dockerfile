FROM python:3.11-slim

WORKDIR /app

# Prevent byte code generation and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SOURCE_DATE_EPOCH=1700000000

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.lock /app/requirements.lock
RUN pip install --no-cache-dir -r requirements.lock

COPY . /app

CMD ["python", "scripts/compile.py", "--output", "PocketGull-Antigravity.ttf"]

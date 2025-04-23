FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY ./app .

RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    gfortran \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel

RUN pip3 install --no-cache-dir -r requirements.txt --verbose

CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8002"]
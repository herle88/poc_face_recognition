# ---------- Stage 1: build frontend ----------
FROM node:20-alpine AS frontend-build
WORKDIR /build
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install
COPY frontend/ .
RUN npm run build

# ---------- Stage 2: install Python deps ----------
FROM python:3.11-slim-bookworm AS pip-build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake gfortran \
    libopenblas-dev liblapack-dev libhdf5-dev \
    libjpeg62-turbo-dev zlib1g-dev libpng-dev \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /tmp/
RUN pip install --no-cache-dir --prefix=/install -r /tmp/requirements.txt

# ---------- Stage 3: runtime (slim) ----------
FROM python:3.11-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    libopenblas0 liblapack3 libhdf5-103-1 \
    libjpeg62-turbo zlib1g libpng16-16 libgl1 libglib2.0-0 \
    curl jq \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from build stage
COPY --from=pip-build /install /usr/local

WORKDIR /app

# Copy backend code
COPY backend/ .

# Copy built frontend
COPY --from=frontend-build /build/dist /app/static

# Copy run script
COPY rootfs/ /
RUN chmod a+x /run.sh

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8099/health || exit 1

CMD ["/run.sh"]

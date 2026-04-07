# ---------- Stage 1: build frontend ----------
FROM node:20-alpine AS frontend-build
WORKDIR /build
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install
COPY frontend/ .
RUN npm run build

# ---------- Stage 2: runtime ----------
FROM python:3.11-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive

# Install system deps for OpenCV / DeepFace + bashio for HA integration
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    libffi-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libpng-dev \
    libtiff-dev \
    libfreetype6-dev \
    libwebp-dev \
    libhdf5-dev \
    curl \
    jq \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Copy built frontend
COPY --from=frontend-build /build/dist /app/static

# Copy run script
COPY rootfs/ /
RUN chmod a+x /run.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8099/health || exit 1

CMD ["/run.sh"]

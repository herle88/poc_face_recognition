ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-debian:bookworm
# ---------- Stage 1: build frontend ----------
FROM node:20-alpine AS frontend-build
WORKDIR /build
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install
COPY frontend/ .
RUN npm run build

# ---------- Stage 2: runtime ----------
FROM ${BUILD_FROM}

ENV DEBIAN_FRONTEND=noninteractive

# Install Python 3.11 and system deps for OpenCV / DeepFace
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
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
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY backend/requirements.txt .
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

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

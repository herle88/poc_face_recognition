ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-python:3.11-alpine3.19
# ---------- Stage 1: build frontend ----------
FROM node:20-alpine AS frontend-build
WORKDIR /build
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install
COPY frontend/ .
RUN npm run build

# ---------- Stage 2: runtime ----------
FROM ${BUILD_FROM}

# Install system deps for OpenCV and building Python packages
RUN apk add --no-cache \
    build-base \
    cmake \
    gfortran \
    openblas-dev \
    libffi-dev \
    jpeg-dev \
    zlib-dev \
    libpng-dev \
    tiff-dev \
    freetype-dev \
    lcms2-dev \
    libwebp-dev \
    hdf5-dev \
    curl

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

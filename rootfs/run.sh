#!/usr/bin/with-contenv bashio

# Get ingress entry for path-based routing
export INGRESS_PATH="$(bashio::addon.ingress_entry)"
export DATA_DIR="/data"

bashio::log.info "Starting DeepFace Recognition add-on..."
bashio::log.info "Ingress path: ${INGRESS_PATH}"

cd /app
exec python3 -m uvicorn main:app --host 0.0.0.0 --port 8099 --log-level info

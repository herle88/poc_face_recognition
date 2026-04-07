#!/usr/bin/env bashio

# Get ingress entry for path-based routing
export INGRESS_PATH="$(bashio::addon.ingress_entry)"
export DATA_DIR="/data"

echo "Starting DeepFace Recognition add-on..."
echo "Ingress path: ${INGRESS_PATH}"

cd /app
exec uvicorn main:app --host 0.0.0.0 --port 8099 --log-level info

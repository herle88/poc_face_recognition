#!/bin/bash
set -e

export DATA_DIR="/data"

# Get ingress path from HA Supervisor API (if running as add-on)
if [ -n "$SUPERVISOR_TOKEN" ]; then
    INGRESS_PATH=$(curl -s -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" \
        http://supervisor/addons/self/info | jq -r '.data.ingress_entry // empty')
    export INGRESS_PATH
    echo "Running as HA add-on, ingress path: ${INGRESS_PATH}"
else
    echo "Running standalone"
fi

cd /app
exec python -m uvicorn main:app --host 0.0.0.0 --port 8099 --log-level info

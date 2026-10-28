#!/usr/bin/env bash
echo "==================================================================="
echo " Neural Topology Mapping - Crowd Analytics System (Phase 2)"
echo "==================================================================="
echo "Starting FastAPI server..."
echo "Usage: ./run.sh [--mock] [--port 8000]"
echo ""
python3 server.py "$@"

#!/bin/bash
# Start the API server
cd /app
source /app/venv/bin/activate
#
sudo uvicorn --host 0.0.0.0 --port 5150 --workers 1 main:app

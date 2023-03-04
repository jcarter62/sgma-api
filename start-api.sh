#!/bin/bash
# Start the API server
cd /app
. venv/bin/activate
#
uvicorn main:app --host 0.0.0.0 --port 5150

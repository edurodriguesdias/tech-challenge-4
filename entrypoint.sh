#!/bin/bash
set -e

# Start mlflow
mlflow ui --host 0.0.0.0 --port 5000 &

# Start evidently
evidently ui --host 0.0.0.0 --port 5001 &

# Wait for all background processes
wait
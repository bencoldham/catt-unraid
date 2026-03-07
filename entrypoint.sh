#!/bin/sh
echo "Scanning for devices..."
catt scan

echo "Starting application..."
exec python main.py
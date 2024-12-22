#!/bin/bash

# Run Kong migrations
echo "Running Kong migrations..."
kong migrations bootstrap || kong migrations up || true

# Start Kong
echo "Starting Kong..."
kong start

# Wait for Kong to be up
echo "Waiting for Kong to start..."
while ! curl -s http://localhost:8001/status; do
    sleep 1
done

echo "Kong is up - configuring services and routes..."

# Run script to configure services and routes
/bin/bash /configure.sh

echo "Kong configuration complete."

# Keep Kong running
tail -f /dev/null

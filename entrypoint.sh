#!/bin/bash
set -e

# Remove X lock files if they exist
rm -f /tmp/.X*-lock

# Start Xvfb with better parameters
Xvfb :99 -screen 0 1920x1080x24 -ac -nolisten tcp &
echo "Waiting for Xvfb to start..."
sleep 3

# Test that Xvfb is working
echo "Testing Xvfb connection..."
xdpyinfo -display :99 >/dev/null 2>&1 || (echo "Xvfb failed to start properly" && exit 1)
echo "Xvfb is running properly"

# Start VNC server for debugging
x11vnc -display :99 \
       -rfbport 5900 \
       -listen 0.0.0.0 \
       -N -forever \
       -passwd secret \
       -shared &
echo "VNC server started on port 5900"

# Instead of automatically running the script, drop into a bash shell
echo "Environment is ready. Use 'python -m app.main' to run the script when you're ready."
echo "Starting bash shell..."

# If a command is provided, execute it, otherwise start bash
if [ $# -eq 0 ]; then
    exec /bin/bash
else
    # Execute the provided command
    echo "Executing provided command: $@"
    exec "$@"
fi
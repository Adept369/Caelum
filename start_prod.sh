#!/bin/bash
# start_prod.sh — Production startup script for Caelum ADHD Assistant

# Make sure to give it execute permission (on Linux/macOS) with:
# chmod +x start_prod.sh



# Set the application port and ngrok domain (if using ngrok for external access)
APP_PORT=5000
NGROK_DOMAIN="https://adhdpapi.ngrok.io"

# Load environment variables from .env file (if available)
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
  echo "✅ Loaded environment variables from .env"
fi

# Create required directories if missing
mkdir -p app/static/audio uploads exports
echo "✅ Required directories ensured."

# (Optional) Start ngrok tunnel if not already running
if ! pgrep -x "ngrok" > /dev/null; then
  echo "🌀 Starting ngrok tunnel on port $APP_PORT..."
  ngrok http --domain="$NGROK_DOMAIN" "$APP_PORT" --log=stdout > ngrok.log 2>&1 &
  sleep 5
else
  echo "🌀 ngrok is already running."
fi

# Display current ngrok tunnel status
echo "🌐 Current ngrok tunnels:"
curl --silent http://127.0.0.1:4040/api/tunnels | python3 -m json.tool

# (Optional) Initialize database tables if the initialization script exists
if [ -f "init_system.py" ]; then
  echo "🛠️ Initializing database tables..."
  python3 init_system.py
fi

# Start the application using Gunicorn as the production server.
# Adjust the number of workers (e.g., --workers 4) and timeout (--timeout 120) as needed.
echo "🚀 Starting Gunicorn server on port $APP_PORT..."
gunicorn run:app --bind 0.0.0.0:"$APP_PORT" --workers 4 --timeout 120

# End of script

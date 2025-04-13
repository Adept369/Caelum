#!/bin/bash
# Enhanced startup script for Caelum's Neurodivergent Assistant Production Environment
# This script loads environment variables, creates required directories,
# starts an ngrok tunnel (if needed), optionally initializes your database, 
# and then starts your Docker Compose services (which run Gunicorn in production mode).

# Application settings
APP_PORT=5000
NGROK_DOMAIN="duck-healthy-easily.ngrok-free.app"

# ----- Load Environment Variables -----
if [ -f .env ]; then
  echo "Loading environment variables from .env..."
  # Export all variables from .env
  set -a
  source .env
  set +a
  echo "✅ Environment variables loaded from .env"
else
  echo "⚠️ No .env file found."
fi

# ----- Ensure Required Directories Exist -----
echo "Ensuring required directories exist..."
mkdir -p app/static/audio uploads exports

# Optionally, attempt to set permissions for the audio directory.
if chmod 777 app/static/audio 2>/dev/null; then
  echo "✅ Set permissions for app/static/audio to 777"
else
  echo "⚠️ Could not change permissions for app/static/audio (this may be unsupported on your OS)."
fi

# ----- Start ngrok Tunnel (if not already running) -----
if ! pgrep -x "ngrok" > /dev/null; then
  echo "🌀 Starting ngrok tunnel on port $APP_PORT..."
  ngrok http --domain=$NGROK_DOMAIN $APP_PORT --log=stdout > ngrok.log 2>&1 &
  sleep 5  # Give ngrok time to establish the tunnel
else
  echo "🌀 ngrok is already running."
fi

# Display current ngrok tunnel status
echo "🌐 Current ngrok tunnels:"
curl --silent http://127.0.0.1:4040/api/tunnels | python3 -m json.tool

# ----- Optional: Initialize Database Tables -----
if [ -f "init_system.py" ]; then
  echo "🛠️ Initializing database tables..."
  python3 init_system.py
fi

# ----- Start Docker Compose -----
echo "🐳 Starting Docker Compose..."
docker compose up --build

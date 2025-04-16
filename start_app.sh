#!/bin/bash
# start_app.sh — Startup script for Caelum ADHD Assistant with ngrok

# Make sure required directories exist
mkdir -p app/static/audio uploads exports

# Start ngrok in the background with your desired URL and port
echo "🌀 Starting ngrok tunnel..."
ngrok http --url=https://adhdpapi.ngrok.io 5000 --log=stdout > ngrok.log 2>&1 &

# Give ngrok a few seconds to establish the tunnel
sleep 5

# (Optional) Display current ngrok tunnels
echo "🌐 ngrok tunnels:"
curl --silent http://127.0.0.1:4040/api/tunnels | python3 -m json.tool

# Start your Flask app using Gunicorn
echo "🚀 Starting Gunicorn..."
gunicorn run:app --bind 0.0.0.0:5000 --timeout 120

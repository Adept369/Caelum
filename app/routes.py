# app/routes.py
import os
import uuid
import sqlite3
import requests
import websocket
import json
from flask import Blueprint, request, jsonify, Response, send_file, stream_with_context
from gtts import gTTS
from twilio.rest import Client
from datetime import datetime
from markdown import markdown
import pdfkit
from app.llm import LLMEngine
from app.config import Config
from twilio.base.exceptions import TwilioRestException

# --- Ensure required directories exist ---
audio_dir = Config.AUDIO_OUTPUT_DIR
if not os.path.exists(audio_dir):
    os.makedirs(audio_dir, exist_ok=True)
# (Permissions adjustment removed for portability)

# Define the blueprint
main = Blueprint('main', __name__)

# === Index Route ===
@main.route('/', methods=['GET'])
def index():
    """
    Index route for the single-user application.
    """
    return "Welcome Lighting Dove to Your Majesty's Royal AI Personal Assistant for ADHD", 200

# Instantiate the LLM engine
llm = LLMEngine()

# Constant for single-user mode (all requests use this user_id)
DEFAULT_USER_ID = "default_user"

# === TWILIO INTEGRATION === 📡
@main.route('/webhook', methods=['POST'])
def webhook():
    """
    Twilio webhook endpoint to receive and respond to incoming messages.
    Processes the incoming message, generates an AI response, converts it to audio using gTTS,
    and sends it back via Twilio.
    """
    sender = request.values.get('From')
    message_body = request.values.get('Body')
    print(f"Received message from {sender}: {message_body}")

    try:
        generated_response = llm.generate_response(message_body)
    except Exception as e:
        print(f"[DEBUG] Error generating LLM response: {e}", flush=True)
        generated_response = "I am sorry, I could not process your request."

    # Generate audio using gTTS and save to file
    audio_filename = f"response_{uuid.uuid4().hex}.mp3"
    audio_path = os.path.join(os.getcwd(), "app", "static", "audio")
    os.makedirs(audio_path, exist_ok=True)
    audio_filepath = os.path.join(audio_path, audio_filename)
    tts = gTTS(generated_response)
    tts.save(audio_filepath)
    media_url = f"https://adhdpapi.ngrok.io/static/audio/{audio_filename}"

    # Send message and audio via Twilio
    client = Client(os.environ.get("TWILIO_ACCOUNT_SID"), os.environ.get("TWILIO_AUTH_TOKEN"))
    twilio_number = os.environ.get("TWILIO_NUMBER")
    client.messages.create(body=generated_response, from_=twilio_number, to=sender)
    client.messages.create(media_url=[media_url], from_=twilio_number, to=sender)

    return Response("<?xml version='1.0' encoding='UTF-8'?><Response></Response>", mimetype='application/xml')

# === GENERIC LLM ENDPOINTS === 🧠
@main.route('/llm', methods=['POST'])
def llm_endpoint():
    """
    Endpoint for processing generic LLM prompts.
    """
    data = request.get_json()
    prompt = data.get("prompt", "")
    if not prompt:
        return Response("No prompt provided", status=400)
    try:
        response_text = llm.generate_response(prompt)
        return Response(response_text, mimetype="text/plain")
    except Exception as e:
        print(f"[DEBUG] Error generating LLM response: {e}", flush=True)
        return Response("Error generating response", status=500)

@main.route('/status', methods=['POST'])
def status_callback():
    """
    Endpoint for processing status callbacks.
    """
    message_sid = request.values.get('MessageSid')
    message_status = request.values.get('MessageStatus')
    error_code = request.values.get('ErrorCode')
    error_message = request.values.get('ErrorMessage')
    print(f"Status update: {message_sid}, {message_status}, {error_code}, {error_message}")
    return Response("Status received", status=200)

# === CAELUM INTEGRATION === 👤
@main.route('/respond', methods=['POST'])
def caelum_respond():
    """
    Endpoint for generating AI responses with fixed personality prompt.
    In single-user mode, the user_id is always DEFAULT_USER_ID.
    """
    data = request.json
    user_input = data.get("input")
    # Ignore provided user_id; always use DEFAULT_USER_ID.
    user_id = DEFAULT_USER_ID
 


# === TEXT-TO-SPEECH SERVICES === 🔊
@main.route('/tts-stream', methods=['POST'])
def tts_stream():
    """
    For this simplified branch, this endpoint generates TTS audio using gTTS and returns the file path.
    (Streaming is not supported with gTTS.)
    """
    data = request.json
    text = data.get("text")
    try:
        audio_file_path = llm.generate_tts_gtts(text)
        return jsonify({"audio_file": audio_file_path}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/tts-download', methods=['POST'])
def tts_download():
    """
    Returns a gTTS-generated MP3 file as a downloadable response.
    """
    data = request.json
    text = data.get("text")
    try:
        audio_file_path = llm.generate_tts_gtts(text)
        return send_file(audio_file_path, mimetype="audio/mpeg", as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

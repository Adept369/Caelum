# tasks.py
import os
import uuid
from celery_app import celery
from twilio.rest import Client
from gtts import gTTS
from app.config import Config

def generate_audio_message(text_response: str) -> str:
    """
    Generates an audio file from the given text using gTTS, saves it to the 
    audio directory, and returns the media URL for the generated audio file.

    Args:
        text_response (str): The text to convert to speech.

    Returns:
        str: The publicly accessible URL for the generated audio file.
    """
    # Generate a unique filename for the audio file.
    audio_filename = f"response_{uuid.uuid4().hex}.mp3"
    audio_dir = os.path.join(os.getcwd(), "app", "static", "audio")
    os.makedirs(audio_dir, exist_ok=True)
    audio_filepath = os.path.join(audio_dir, audio_filename)
    
    # Generate the audio file using gTTS.
    tts = gTTS(text_response)
    tts.save(audio_filepath)
    
    # Construct the media URL using the static domain defined in Config.
    # If Config does not define STATIC_DOMAIN, it defaults to the provided domain.
    static_domain = getattr(Config, "STATIC_DOMAIN", "https://adhdpapi.ngrok.io")
    media_url = f"{static_domain}/static/audio/{audio_filename}"
    return media_url

def send_twilio_message(body: str, recipient: str, media_url: str) -> str:
    """
    Sends a message via Twilio with the given message body and media URL.

    Args:
        body (str): The text message to send.
        recipient (str): The recipient's phone number.
        media_url (str): The URL to the media (audio file).

    Returns:
        str: The Twilio message SID.
    """
    client = Client(os.environ.get("TWILIO_ACCOUNT_SID"), os.environ.get("TWILIO_AUTH_TOKEN"))
    twilio_number = os.environ.get("TWILIO_NUMBER")
    status_callback = getattr(Config, "STATUS_CALLBACK_URL", "https://adhdpapi.ngrok.io/status")
    message = client.messages.create(
        body=body,
        media_url=[media_url],
        from_=twilio_number,
        to=recipient,
        status_callback=status_callback
    )
    return message.sid

@celery.task
def send_morning_affirmation(recipient: str) -> str:
    """
    Celery task that sends a morning affirmation via Twilio.

    Args:
        recipient (str): The recipient's phone number.

    Returns:
        str: The Twilio message SID.
    """
    affirmation = "Good morning! You are capable, resilient, and ready to seize the day!"
    media_url = generate_audio_message(affirmation)
    return send_twilio_message(affirmation, recipient, media_url)

@celery.task
def send_evening_reflection(recipient: str) -> str:
    """
    Celery task that sends an evening reflection message via Twilio.

    Args:
        recipient (str): The recipient's phone number.

    Returns:
        str: The Twilio message SID.
    """
    reflection = ("Good evening. Take a moment to reflect on your day, celebrate your victories, "
                  "and learn from your challenges.")
    media_url = generate_audio_message(reflection)
    return send_twilio_message(reflection, recipient, media_url)

@celery.task
def send_focus_time_suggestion(recipient: str) -> str:
    """
    Celery task that sends a focus time suggestion via Twilio.

    Args:
        recipient (str): The recipient's phone number.

    Returns:
        str: The Twilio message SID.
    """
    suggestion = (
        "This is your moment for focused self-improvement. "
        "Consider spending 15 minutes in quiet reflection, reading an inspiring article, "
        "or planning your next step towards a better tomorrow."
    )
    media_url = generate_audio_message(suggestion)
    return send_twilio_message(suggestion, recipient, media_url)

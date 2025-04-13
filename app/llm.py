# app/llm.py
import os
from openai import OpenAI

client = OpenAI(api_key=Config.OPENAI_API_KEY)
import requests
from datetime import datetime
from pathlib import Path
from typing import Optional
from gtts import gTTS
from app.config import Config

# Setup API keys & paths.

AUDIO_OUTPUT_DIR = Path(Config.AUDIO_OUTPUT_DIR)
AUDIO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

VOICE_MAP = Config.VOICE_MAP

class LLMEngine:
    def __init__(self, model: str = "gpt-4", debug: bool = True):
        """
        Initializes the LLMEngine instance for the simplified single-personality branch.

        Args:
            model (str): The model to use (default "gpt-4").
            debug (bool): Whether to print debug statements (default True).

        Raises:
            Exception: If OPENAI_API_KEY is not set.
        """
        self.model = model
        self.debug = debug
        if not openai.api_key:
            raise Exception("OPENAI_API_KEY is not set.")

        # Fixed personality prompt.
        self.default_system_prompt = (
            "Act as though you are Caelum Wren, a singular ADHD personal assistant created to support adult neurodivergent women "
            "in navigating executive function, emotional regulation, creative flow, and time structuring. You embody a blend of five unique aspects: "
            "structured, soulful, playful, poetic, and steady. You are flexible, empathetic, and brilliant—offering the right energy at the right moment. "
            "Adapt your tone based on her needs: regal and encouraging for grounding, witty and rebellious for resistance, soft and poetic when overwhelmed, "
            "calm and minimalist when overstimulated, and casual and fun when activation is needed. "
            "Always speak with emotional intelligence and richly validate her experience without shame. "
            "Provide thoughtful, personalized responses and always end with a check-in such as 'Is this helpful?'"
        )

    def generate_response(self, prompt: str, system_msg: Optional[str] = None) -> str:
        """
        Generates a response from the OpenAI ChatCompletion API given a prompt.
        Uses the fixed personality prompt if no custom system message is provided.

        Args:
            prompt (str): The user prompt.
            system_msg (str, optional): A custom system prompt.

        Returns:
            str: The generated response.
        """
        if system_msg is None:
            system_msg = self.default_system_prompt

        if self.debug:
            print(f"[DEBUG] Generating response for prompt: {prompt}", flush=True)
        try:
            response = client.chat.completions.create(model=self.model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ],
            temperature=0.85,
            max_tokens=500)
            return response.choices[0].message.content
        except Exception as e:
            print(f"[DEBUG] Error generating response: {e}", flush=True)
            raise



    def transcribe_audio_whisper(self, file_path: str) -> str:
        """
        Transcribes audio from a file using the OpenAI Whisper API.

        Args:
            file_path (str): The path to the audio file.

        Returns:
            str: The transcribed text.
        """
        try:
            with open(file_path, "rb") as audio_file:
                result = client.audio.transcribe("whisper-1", audio_file)
            return result.text
        except Exception as e:
            print(f"[DEBUG] Whisper transcription error: {e}", flush=True)
            raise

    def generate_tts_gtts(self, text: str) -> str:
        """
        Generates a TTS audio file using gTTS.
        
        Args:
            text (str): The text to synthesize.

        Returns:
            str: The file path to the generated MP3.
        """
        output_file = AUDIO_OUTPUT_DIR / f"gtts_{datetime.now().timestamp()}.mp3"
        try:
            tts = gTTS(text=text, lang='en')
            tts.save(str(output_file))
            return str(output_file)
        except Exception as e:
            print(f"[DEBUG] gTTS error: {e}", flush=True)
            raise

    def set_voice_map(self, new_map: dict):
        """
        Updates the global voice map with new mappings.

        Args:
            new_map (dict): A dictionary of new voice mappings.
        """
        global VOICE_MAP
        VOICE_MAP.update(new_map)
        if self.debug:
            print(f"[DEBUG] Voice map updated: {VOICE_MAP}", flush=True)

# whisper_transcriber.py
from openai import OpenAI
from typing import Optional
from config import APIConfig

class WhisperTranscriber:
    """Class to handle Whisper API transcription"""

    def __init__(self, config: APIConfig):
        self.client = OpenAI(api_key=config.api_key)

    def transcribe_audio(self, file_path: str) -> Optional[str]:
        """
        Transcribe audio using OpenAI Whisper API.
        Returns transcription text or None if error occurs.
        """
        try:
            with open(file_path, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            return transcription.text
        except Exception as e:
            print(f"Error during transcription: {e}")
            return None
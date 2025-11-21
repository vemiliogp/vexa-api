"""Transcription service module."""

from dataclasses import dataclass

from whisper import Whisper, load_model


@dataclass
class TranscriptionService:
    """Service for handling audio transcriptions."""

    model = "base"
    client: Whisper = load_model(model)

    def transcribe(self, audio_file_path: str) -> str:
        """Transcribe the given audio file and return the text."""

        try:
            result = self.client.transcribe(audio_file_path)
            return {"transcription": result["text"]}
        except Exception as e:
            raise e

"""Transcription service module."""

from dataclasses import dataclass
from os import path, remove
from tempfile import NamedTemporaryFile

from fastapi import File
from whisper import Whisper, load_model


@dataclass
class TranscriptionService:
    """Service for handling audio transcriptions."""

    model: str = "base"
    client: Whisper = load_model(model, device="cpu")

    async def transcribe(self, file: File) -> dict:
        """Transcribe the given audio file and return the text."""

        with NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        try:
            result = self.client.transcribe(tmp_path, fp16=False)
            return {"transcription": result["text"]}
        except Exception as e:
            raise e
        finally:
            if path.exists(tmp_path):
                remove(tmp_path)

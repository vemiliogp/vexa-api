"""Text-to-Speech service module."""

from dataclasses import dataclass
from logging import info
from os import path, remove
from tempfile import NamedTemporaryFile

from edge_tts import Communicate


@dataclass
class TTSService:
    """Service for handle tts synthesis."""

    voice: str = "es-ES-AlvaroNeural"
    rate: str = "+0%"

    async def synthesize(self, text: str) -> bytes:
        """Convert text to speech and return audio bytes."""

        try:
            communicate = Communicate(text=text, voice=self.voice, rate=self.rate)

            with NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tmp_path = tmp.name
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        tmp.write(chunk["data"])

            with open(tmp_path, "rb") as audio_file:
                audio_bytes = audio_file.read()

            info(f"TTS synthesis completed: {len(audio_bytes)} bytes")
            return audio_bytes

        except Exception as e:
            info(f"TTS synthesis failed: {e}")
            raise e
        finally:
            if path.exists(tmp_path):
                remove(tmp_path)

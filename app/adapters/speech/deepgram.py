import io
import wave
from openai import AsyncOpenAI
from app.infrastructure.config import settings
from app.infrastructure.logger import get_logger


logger=get_logger(__name__)

RATE=16000
CHANNELS=1
SAMPWIDTH = 2

class STTAdapter:
    def __init__(self):
        self.client=AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def transcribe(self, audio_bytes: bytes)-> str:
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(SAMPWIDTH)
            wf.setframerate(RATE)
            wf.writeframes(audio_bytes)
        wav_buffer.seek(0)
        wav_buffer.name = "audio.wav"

        response=await self.client.audio.transcriptions.create(
            model="whisper-1", 
            file=wav_buffer,
            language="ur"
        )
        transcript=response.text.strip()
        logger.info(f"Transcribed : {transcript}")
        return transcript

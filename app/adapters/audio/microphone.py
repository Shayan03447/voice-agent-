import pyaudio
import asyncio
from typing import AsyncGenerator
from app.infrastructure.logger import get_logger
from app.application.audio_pipeline import AudioPipeline

logger=get_logger(__name__)

CHUNK= 1024
FORMAT= pyaudio.paInt16
CHANNEL=1
RATE=16000

class MicrophoneInput:
    def __init__(self):
        self.pipeline=AudioPipeline()
        self.audio= pyaudio.PyAudio()

    async def listen(self)-> AsyncGenerator[bytes, None]:
        stream= self.audio.open(
            format=FORMAT,
            channels= CHANNEL,
            rate= RATE,
            input= True,
            frame_per_buffer=CHUNK
        )
        logger.info("Microphone listening")
        try:
            while True:
                chunk=await asyncio.get_event_loop().run_in_executor(
                    None, stream.read, CHUNK
                )
                utterance=self.pipeline.process_audio_chunk(chunk)
                if utterance is not None:
                    logger.info(f"Utterance ready: {len(utterance)} bytes")
                    yield utterance
        finally:
            stream.stop_stream()
            stream.close()
            self.audio.terminate()

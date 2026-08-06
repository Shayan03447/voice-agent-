import pyaudio
import wave
import io
from app.infrastructure.logger import get_logger

logger=get_logger(__name__)

class SpeakerOutput:
    def play_wav(self, audio_bytes)-> None:
        audio=pyaudio.PyAudio()
        with wave.open(io.BytesIO(audio_bytes)) as wf:
            stream=audio.open(
                format=audio.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True
            )
            data=wf.readframes(1024)
            while data:
                stream.write(data)
                data=wf.readframe(1024)

            stream.stop_stream()
            stream.close()
        audio.terminate()
        logger.info("Audio Played")
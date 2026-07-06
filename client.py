import asyncio
import pyaudio
import websockets

# ==========================
# Audio Configuration
# ==========================

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

WEBSOCKET_URL = "ws://127.0.0.1:8000/voice/incoming"


async def stream_microphone():
    print("Opening microphone...")

    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    print("Connecting to WebSocket...")

    async with websockets.connect(WEBSOCKET_URL) as websocket:
        print("Connected")

        try:
            while True:
                # Read microphone audio
                chunk = stream.read(
                    CHUNK,
                    exception_on_overflow=False
                )

                # Send raw bytes
                await websocket.send(chunk)

                # Small delay
                await asyncio.sleep(0.01)

        except KeyboardInterrupt:
            print("Stopping")

        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()


if __name__ == "__main__":
    asyncio.run(stream_microphone())
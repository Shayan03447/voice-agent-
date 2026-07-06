from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.application.audio_pipeline import AudioPipeline

router= APIRouter()
pipeline=AudioPipeline()

@router.websocket("/voice/incoming")
async def media_stream(websocket: WebSocket):
    await websocket.accept()
    print("websocket connection")

    try:
        while True:
            # Recieve one audio chunk
            chunk = await websocket.receive_bytes()
            # Pass chunk to pipeline
            complete_audio=pipeline.process_audio_chunk(chunk)

            # if pipeline say audio is ready
            if complete_audio is not None:
                print(f"complete audio ready: {len(complete_audio)} bytes")
            await websocket.send_text("ok")

    except WebSocketDisconnect:
        print("Websocket Disconnected")



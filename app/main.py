from fastapi import FastAPI
from app.api.websockets.media_stream import router as media_router

app=FastAPI()
app.include_router(media_router)

@app.get("/")
def health_check():
    return {"status":"ok"}

print("MEDIA ROUTER LOADED")

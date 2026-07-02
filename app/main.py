from fastapi import FastAPI
from app.api.voice import router as voice_router

app=FastAPI()
app.include_router(voice_router)

@app.get("/")
def health_check():
    return {"status":"ok"}

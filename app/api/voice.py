from fastapi import APIRouter, Request
from app.adapters.telephony.twilio import generate_twiml_response

router=APIRouter()
@router.post("/voice/incoming")
async def incoming_call(request: Request):
    twiml=generate_twiml_response(message="Hello, thanks for calling Hill Thrill")
    return twiml
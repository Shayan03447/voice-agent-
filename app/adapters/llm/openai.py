from dataclasses import dataclass
from openai import AsyncOpenAI
from app.infrastructure.config import settings
from app.infrastructure.logger import get_logger

logger= get_logger(__name__)

@dataclass
class ToolCalls:
    name: str
    arguments: dict
    call_id: str

class LLMAdaptor:
    def __init__(self):
        self.client=AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
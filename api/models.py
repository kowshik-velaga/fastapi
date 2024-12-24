from pydantic import BaseModel

class SentimentResult(BaseModel):
    id: int
    text: str
    sentiment: str

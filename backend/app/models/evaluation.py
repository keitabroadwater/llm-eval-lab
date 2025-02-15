from pydantic import BaseModel

class EvaluationRequest(BaseModel):
    prompt: str
    response: str

class EvaluationResponse(BaseModel):
    prompt: str
    response: str
    score: int
    explanation: str

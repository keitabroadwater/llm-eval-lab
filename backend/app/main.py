from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.evaluation import EvaluationRequest, EvaluationResponse
from app.evaluation.llm_as_judge import evaluate_with_gpt4

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def read_root():
    return {"message": "LLM Evaluation Backend Running!"}


@app.post("/evaluate", response_model=EvaluationResponse)
def evaluate_prompt(request: EvaluationRequest):
    evaluation_result = evaluate_with_gpt4(request.prompt, request.response)
    return EvaluationResponse(
        prompt=request.prompt,
        response=request.response,
        score=evaluation_result["score"],
        explanation=evaluation_result["explanation"]
    )

from openai import OpenAI
import os
from dotenv import load_dotenv

# Get the absolute path to the .env file
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(os.path.dirname(os.path.dirname(current_dir)), '.env')

# Load environment variables
load_dotenv(dotenv_path=env_path)

# Debug: Print paths and API key status
print(f"Looking for .env at: {env_path}")
api_key = os.getenv("OPENAI_API_KEY")
print(f"API key loaded: {'Yes' if api_key else 'No'}")

# Initialize client with explicit API key
client = OpenAI(api_key=api_key)

def evaluate_with_gpt4(prompt: str, response: str) -> dict:
    evaluation_prompt = f"""
    You are an evaluator assessing the quality of an AI-generated response to a user prompt.
    Evaluate the response based on:
    - Relevance
    - Helpfulness
    - Detail

    Use a scale from 1 to 4:
    1 = Irrelevant
    2 = Relevant but not helpful
    3 = Relevant and helpful, but could be more detailed
    4 = Relevant, helpful, and detailed

    Prompt: {prompt}
    Response: {response}

    Please explain your evaluation and give a final score (1-4).
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": evaluation_prompt}]
        )
        evaluation_output = completion.choices[0].message.content
        score = extract_score_from_text(evaluation_output)
        return {"score": score, "explanation": evaluation_output}
    except Exception as e:
        return {"score": 0, "explanation": f"Error: {str(e)}"}
    
    
def extract_score_from_text(text: str) -> int:
    """
    Very basic extraction - looks for the final score in the GPT output.
    You can make this more robust later.
    """
    for i in range(4, 0, -1):
        if f"{i}" in text:
            return i
    return 0  # If we can't extract a score, default to 0

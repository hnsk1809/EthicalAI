from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

# Define request model
class UserChoices(BaseModel):
    user_id: str
    choices: list[str]  # List of user-selected ethical choices

# Dummy Mistral API URL (replace with actual URL)
MISTRAL_API_URL = "https://api.mistral.ai/analyze"

@app.post("/analyze")
async def analyze_choices(data: UserChoices):
    """
    Receives user choices, sends them to Mistral AI, and returns insights.
    """
    mistral_payload = {"user_id": data.user_id, "choices": data.choices}

    try:
        # Send request to Mistral API
        response = requests.post(MISTRAL_API_URL, json=mistral_payload)

        # Handle API response
        if response.status_code == 200:
            insights = response.json()
            return {"status": "success", "insights": insights}
        else:
            raise HTTPException(status_code=response.status_code, detail="Mistral API error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Root endpoint
@app.get("/")
def root():
    return {"message": "FastAPI backend is running!"}

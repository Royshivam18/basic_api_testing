import os
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Read the API key from environment variables. Falls back to a default for local testing.
API_KEY = os.getenv("API_KEY", "my-super-secret-key-123")

# Define the structure of the incoming JSON data
class AdditionRequest(BaseModel):
    num1: float
    num2: float

@app.get("/")
def home():
    return {"message": "Python backend is alive! Use POST /api/add to add numbers."}

@app.post("/api/add")
def add_numbers(payload: AdditionRequest, x_api_key: str = Header(None)):
    # Verify the API key from headers (FastAPI converts X-API-Key to x_api_key automatically)
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid or missing API Key.")
    
    total = payload.num1 + payload.num2
    
    return {
        "success": True,
        "operation": f"{payload.num1} + {payload.num2}",
        "result": total
    }
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from a .env file (for local development)
load_dotenv()

# Set OpenAI API key securely from an environment variable
OpenAI.api_key = os.getenv("OPENAI_API_KEY")  # Load the API key from the environment
#openai.api_key = os.getenv("OPENAI_API_KEY")
if OpenAI.api_key is None:
    raise ValueError("OPENAI_API_KEY not set in environment variables.")

# Define your own API token for securing your endpoints
MY_API_TOKEN = os.getenv("MY_API_TOKEN")
if MY_API_TOKEN is None:
    raise ValueError("MY_API_TOKEN not set in environment variables.")

# Dependency for API key authentication using the Authorization header
api_key_header = APIKeyHeader(name="Authorization")

def get_api_key(api_key: str = Depends(api_key_header)):
    # Expecting the header to be "Bearer <token>" or just "<token>"
    token = api_key.split(" ")[1] if " " in api_key else api_key
    if token != MY_API_TOKEN:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return token

# Initialize FastAPI app
app = FastAPI(
    title="Summary Generator API",
    description="An API to generate summaries using a generative AI model.",
    version="1.0.0"
)

# Define the request model
class SummaryRequest(BaseModel):
    data: str  # The financial data (or other type of data) to summarize

# Define the response model
class SummaryResponse(BaseModel):
    summary: str

@app.post("/health-summary", response_model=SummaryResponse)
def health_summary(request: SummaryRequest, api_key: str = Depends(get_api_key)):
    try:
        # Define the system and user messages using the request data
        system_message = "You are a life advisor who recommends actions to enhance quality of life based on best practices. Each recommendation should consider a person’s satisfaction and importance ratings (scale 1–10) for the following dimensions: Job & Career: Fulfillment, growth, work-life balance; Physical Health: Fitness, nutrition, sleep; Mental Health: Stress management, mindfulness; Significant Other: Communication, intimacy, support; Family: Closeness, support, conflict resolution; Friendship: Trust, shared experiences; Community: Engagement, volunteerism; Spirituality & Faith: Beliefs, purpose; Physiological Needs: Basic needs (food, shelter, sleep); Finances: Budgeting, saving, debt management; Education & Learning: Personal growth, skill development; Hobbies & Entertainment: Joyful activities outside work."
        user_message = f"I'm looking for advice on improving my quality of life. Here are my current ratings for each dimension (satisfaction and importance on a scale from 1 to 10):\n{request.data}"

        # Create a client instance
        client = OpenAI()

        # Make the API call to OpenAI
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            model='gpt-4o-mini',
            temperature=0.7  # Adjust for creativity level
        )

        summary = response.choices[0].message.content.strip()
        return SummaryResponse(summary=summary)
    
    except client.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

@app.post("/data-summary", response_model=SummaryResponse)
def data_summary(request: SummaryRequest, api_key: str = Depends(get_api_key)):
    try:
        # Define the system and user messages using the request data
        system_message = "You are an expert in data analysis..."
        user_message = f"Data:\n{request.data}"

        # Create a client instance
        client = OpenAI()

        # Make the API call to OpenAI
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            model='gpt-4o-mini',
            temperature=0.7
        )

        summary = response.choices[0].message.content.strip()
        return SummaryResponse(summary=summary)
    
    except client.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

import os
from openai import AzureOpenAI
from pydantic import BaseModel
from fastapi import HTTPException
from typing import Dict, Any
# # Environment variables
# api_key = os.environ.get("AZURE_API_KEY")
# api_version = os.environ.get("API_VERSION")
# azure_endpoint = os.environ.get("AZURE_BASE_URL")
# deployment_model = os.environ.get("AZURE_DEPLOYEMENT_NAME")
# temperature = os.environ.get("TEMPERATURE")
# max_tokens = os.environ.get("MAX_TOKENS")

from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
# Get the credentials
azure_endpoint = os.getenv("AZURE_ENDPOINT")
deployment_model = os.getenv("DEPLOYMENT_MODEL")
deployment = os.getenv("DEPLOYMENT_MODEL_NAME")
api_key = os.getenv("API_KEY")
api_version = os.getenv("API_VERSION")

temperature = 0.9
max_tokens = 2000


# Initialize AzureOpenAI client
client = AzureOpenAI(
    azure_endpoint=azure_endpoint,
    api_key=api_key,
    api_version=api_version,
)

# Request/Response models
class SummarizationRequest(BaseModel):
    input_data: Dict[str, Any] = {} 

class SummarizationResponse(BaseModel):
    summary: str

# Summarization function
def summarize(request: SummarizationRequest):
    try:
        data = request.input_data
        print("Data from DB:", data)
        system_prompt = (
            "You are a summarizer responsible for consolidating information collected from multiple data sources into a unified summary. "
            "Your task is to analyze the data comprehensively and generate a single, cohesive summary based on the different topics discussed in the conversations. Do not categorize the summary based on the input source data."
            "If content is not there then give a mesage like 'No email data found for this client, please check the client ID and try again' frame the sentence based on the user query."
        )

        response = client.chat.completions.create(
            model=deployment_model,
            messages=[
                { "role": "system", "content": system_prompt },
                { "role": "user", "content": str(data) }
            ],
            max_tokens=int(max_tokens),
            temperature=float(temperature),
        )

        summary_text = response.choices[0].message.content
        print("Summary:", summary_text)
        return SummarizationResponse(summary=summary_text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization error: {str(e)}")
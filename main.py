from fastapi import FastAPI
from pydantic import BaseModel
from function_calling_agent import fn_call
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from summarization import summarize, SummarizationRequest, SummarizationResponse
from inference import recommendation


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define the input data model
class UserInput(BaseModel):
    question: str

# Endpoint to accept input and return a response
@app.post("/greet")
def greet_user(user_input: UserInput):
    response = fn_call(user_input.question)
    return {
        #"message": f"Hello {user_input.name}, you are {user_input.age} years old!"
        "message" : f"Chatbot : {response}"
    }

@app.post("/summarize", response_model=SummarizationResponse)
def summarize_text(request: SummarizationRequest):
    return summarize(request)

class RecommendationRequest(BaseModel):
    client_id: str

@app.post("/recommend")
def recommend_product(user_input: RecommendationRequest):
    recommend = recommendation(user_input.client_id)
    return {
        #"message": f"Hello {user_input.name}, you are {user_input.age} years old!"
        "message" : f"Chatbot : {recommend}"
    }


from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get the credentials
azure_endpoint = os.getenv("AZURE_ENDPOINT")
deployment_model = os.getenv("DEPLOYMENT_MODEL")
model_name = os.getenv("DEPLOYMENT_MODEL_NAME")
api_key = os.getenv("API_KEY")
api_version = os.getenv("API_VERSION")



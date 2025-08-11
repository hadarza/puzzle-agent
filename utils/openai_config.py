from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
llm = ChatOpenAI(temperature=0, model_name="gpt-4o", api_key=os.environ.get("OPENAI_API_KEY"))

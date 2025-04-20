from dotenv import load_dotenv
import os
from langchain.llms import HuggingFaceHub
from huggingface_hub import login

# Load .env file
load_dotenv()

# Login to HuggingFace
os.environ['hugging_face_apiKey'] = os.getenv('hugging_face_apiKey')

# Initialize Hugging Face LLM (this works great with text generation models)
llm = HuggingFaceHub(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    model_kwargs={"temperature": 0.7, "max_new_tokens": 256}
)

# Ask a question
prompt = "My name is John. Who are you?"
response = llm.invoke(prompt)

print("Response:\n", response)

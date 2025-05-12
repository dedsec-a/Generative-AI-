from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import  os 
from dotenv import load_dotenv
from langserve import add_routes
load_dotenv()


grok_api_key = os.getenv("GROQ_API_KEY")
model = ChatGroq(model="Gemma2-9b-It",groq_api_key= grok_api_key)


# Creating a ChatPrompt Template 
system_template = "Translate the Following into {language}:"
prompt_template = ChatPromptTemplate.from_messages(
    [
        ('system',system_template),
        ('user','{text}')
    ]

)

parser = StrOutputParser()

# Making a Chain 
chain = prompt_template|model|parser


# App Defenation
app = FastAPI(title="Langchain Server",version="1.0",description="A Simple API Server using Langchain runnable Interface")
add_routes(
    app,
    chain,
    path="/chain"

)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app,host="localhost",port=8000)


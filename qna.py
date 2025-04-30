import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
import os 
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


# Langsmith Trakcing 
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Simple Q&A Chatbot with ollama"


# Chat Prompt Template 
promt = ChatPromptTemplate.from_messages(
    [
        ("system","You are a Helpful assistant . Please response to the user queries"),
        ("user","Question:{question}")
    ]
) 

def generate_response(question,engine):
    llm  = OllamaLLM(model = engine)
    output_parser = StrOutputParser()
    chain = promt|llm|output_parser
    answer = chain.invoke({'question':question})
    return answer 


# StreamLit App

st.title("Simple Q&A ChatBot Using Ollama")


st.sidebar.title("Please Enter the Engine")
engine = st.sidebar.selectbox("Select the LLM Model",["gemma2:2b","gemma:2b","starcoder2:3b"])

# Adjust response Time 
temperature = st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max_Tokens",min_value=50,max_value=300,value=150)

# Main User Interface 6
st.write("Ask your Question")
user_input = st.text_input("You")
if user_input:
  response = generate_response(user_input,engine=engine)
  st.write(response)
else:
   st.write("Please Provide an input")


    
    



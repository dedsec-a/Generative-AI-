import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
# <---------------Imports---------------------------->

#Initlaise the Environment to get the LangChain Tracing and APi keys
load_dotenv()

os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Simple Q&A ChatBot Using Groq"

# <-----------------Environment Setup--------------------------->


# Defining the Prompt 

prompt = ChatPromptTemplate(
    [
        ('system',"you are a helpful assistant . Please respond to the Queries of the User"),
        ('user',"Question:{question}")
    ]
)

# <---------------Prompt Template----------------------->

 # Defining the Function to Get the Chat

def generate_response(llm,api_key,question):
 model  = ChatGroq(api_key=api_key,model=llm)
 output_parser = StrOutputParser()
 chain = prompt|model|output_parser
 response = chain.invoke({'question':question})
 return response

# <---------Geneerator Funtion is Done------------------>

# Deifing the Streamlit app

st.title("Simple Question and Answer ChatBot Using Groq")
st.sidebar.title("Try your LLM")
api_key = st.sidebar.text_input("Please Enter your Groq API Key",type="password")

st.sidebar.title("please Choose your LLM Model")
llm = st.sidebar.selectbox("Choose you LLM model",["llama-3.3-70b-versatile","llama-3.1-8b-instant","gemma2-9b-it"])


# Writing the Main Interface
st.write("Please Enter your Question")
user_input = st.text_input("you")

if user_input:
 response = generate_response(llm=llm,api_key=api_key,question=user_input)
 st.write(response)
else:
 st.write("Please provide a Valid Input")




    

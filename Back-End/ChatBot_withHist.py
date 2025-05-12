from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
from langserve import add_routes
from fastapi import FastAPI
from langchain_core.messages import HumanMessage , SystemMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

load_dotenv() # initlaised the Dot-Env 

groq_api_key = os.getenv("GROQ_API_KEY")



model = ChatGroq(model="Gemma2-9b-It",groq_api_key = groq_api_key)

result = model.invoke([HumanMessage(content="Hii My Name is Harsh and I am an Generative AI Enginner")])

# Making the ChatHistory Feature

store = {}

def get_session_history(session_id:str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]
with_message_history = RunnableWithMessageHistory(model,get_session_history=get_session_history)


config1 = {"configurable":{"session_id":"s001"}}
config2 = {"configurable":{"session_id":"s002"}}

result1 = with_message_history.invoke(
    [HumanMessage(content="Can you Plan a Trip to Paris")],
    config=config1
)

result2 = with_message_history.invoke(
    [
        HumanMessage(content= "Hii My Name is Harsh Kumar and i am working on Making Chatbots")
    ], config=config2
)

result3 = with_message_history.invoke(
    [
        HumanMessage(content="do you Remember My Name")
    ],config=config2
)






print(result3)
print(result3.content)


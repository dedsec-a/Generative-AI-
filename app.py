import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader  # Loading the Text
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.llms import ollama
import streamlit as st 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# Setting up the Environment 
load_dotenv()
os.environ['hugging_face_apiKey'] = os.getenv('hugging_face_apiKey')
os.environ["OLLAMA_FORCE_CPU"] = "true"

# Converting into Documents
loaders = TextLoader('speech.txt',encoding='utf-8')
documnets = loaders.load()
# Spliting the Documents
text_spliter = CharacterTextSplitter(chunk_size = 200 , chunk_overlap = 30)
docs = text_spliter.split_documents(documents=documnets)
# Creating Ollma Embeddings

embedding = HuggingFaceEmbeddings(model_name = 'all-miniLM-l6-v2')
db = FAISS.from_documents(docs,embedding=embedding)
db

query = "how do we cultivate perseverance in our own lives"

docs = db.similarity_search_with_score(query=query)

print(docs)

db.save_local('index.faiss')

prompt = ChatPromptTemplate.from_messages(
    [
        ('system',"you are a scientist whoose work is to study the cesmic activity of the earth you are not allowed to answer anything else .Please Answer Accordingly"),
        ('user','Question:{question}')
    ]
)


# Streamlit
st.title("Gen Ai App ")

input_text = st.text_input("What would you like to know about the Earth's Cesmic Activiy ")

llm = ollama.Ollama(model="gemma:2b") 

output_parser = StrOutputParser()
chain = prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({'question':input_text}))



    







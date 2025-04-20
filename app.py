import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader  # Loading the Text
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# Setting up the Environment 
load_dotenv()
os.environ['hugging_face_apiKey'] = os.getenv('hugging_face_apiKey')

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





    







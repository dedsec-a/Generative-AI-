from langchain_community.document_loaders import TextLoader
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
import os 
import Spliter

# <------------------Imports------------------------>
load_dotenv()

os.environ('hugging_face_apikey') = os.getenv('hugging_face_apikey')


class embedding:
    def __init__(self,documents):
        self.documents = documents
        self.embedder =  HuggingFaceEmbeddings()

    def embeeded(self):
        embeded_docs = self.embedder.embed_query(self.documents)
        return embeded_docs
    




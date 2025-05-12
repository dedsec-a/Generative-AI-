# let's say we are Making a Class called Slpitter Class Whcih takes a .txt files and makes it in doc from and then Splits it using Recurcive text splitter 
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class Splitter:
    def __init__(self, text_file: str, chunk_size: int, chunk_overlap: int):
        self.text_file = text_file
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_loader = TextLoader(self.text_file,encoding='utf-8')
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)

    def load_doc(self):
        loaded_doc = self.text_loader.load()
        print(f"Loaded document: {loaded_doc}")  # Debugging
        return loaded_doc

    def split_doc(self):
        print("Loading document...")
        doc_content = self.load_doc()
        print("Document loaded successfully.")

        print("Splitting document now...")
        final_docs = self.text_splitter.split_documents(doc_content)
        print("Split result:", final_docs)  # Debugging output
        return final_docs



import faiss
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()
# Load the OpenAI API key from the environment variables

# Initialize the OpenAIEmbeddings class with the loaded API key
embeddings = OpenAIEmbeddings()

class FAISSDatabase:
    def __init__(self, folder_path, index_name, embeddings):
        self.folder_path = folder_path
        self.index_name = index_name
        self.embeddings = embeddings
        self.db = self.load_db()

    def load_db(self):
        return FAISS.load_local(
            folder_path=self.folder_path,
            index_name=self.index_name,
            embeddings=self.embeddings,
            allow_dangerous_deserialization=True,
        )

    def save_db(self):
        self.db.save_local(folder_path=self.folder_path, index_name=self.index_name)

# Usage example:
# Initialize the FAISSDatabase class
faiss = FAISSDatabase(folder_path="faiss_db", index_name="faiss_index", embeddings=embeddings)
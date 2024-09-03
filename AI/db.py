import faiss
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

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
faiss = FAISSDatabase(folder_path="faiss_db", index_name="faiss_index", embeddings=OpenAIEmbeddings())
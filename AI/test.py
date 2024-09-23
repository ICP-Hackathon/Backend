from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv
import faiss


load_dotenv()

# 임베딩
embeddings = OpenAIEmbeddings()
dimension_size = len(embeddings.embed_query("hello world"))
print(dimension_size)
db = FAISS(
    embedding_function=OpenAIEmbeddings(),
    index=faiss.IndexFlatL2(dimension_size),
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

db.save_local(folder_path="faiss_db", index_name="faiss_index")

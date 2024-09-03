from dotenv import load_dotenv
import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

load_dotenv()

# 임베딩
embeddings = OpenAIEmbeddings()

# 임베딩 차원 크기를 계산
# dimension_size = len(embeddings.embed_query("hello world"))
# print(dimension_size)

# db = FAISS.from_texts(
#     ["안녕하세요. 정말 반갑습니다.", "제 이름은 테디입니다."],
#     embedding=OpenAIEmbeddings(),
#     metadatas=[{"source": "user1"}, {"source": "user1"}],
#     ids=["user1_2024.08.28", "user1_2024.08.29"],
# )
# print(db.index_to_docstore_id)
# print(db.docstore._dict)

# db.add_texts(
#     ["이번엔 텍스트 데이터를 추가합니다."],
#     metadatas=[{"source": "user2"}],
#     ids=["user2_2024.08.29"],
# )

# db.save_local(folder_path="faiss_db", index_name="faiss_index")

db = FAISS.load_local(
    folder_path="faiss_db",
    index_name="faiss_index",
    embeddings=embeddings,
    allow_dangerous_deserialization=True,
)

print(db.index_to_docstore_id)
print(db.docstore._dict)
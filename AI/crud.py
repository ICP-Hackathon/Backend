from db import faiss

# 데이터베이스에 새 텍스트를 추가하는 함수
def add_text(texts, metadatas, ids):
    faiss.db.add_texts(texts, metadatas=metadatas, ids=ids)
    print(f"Added {len(texts)} text(s) to the database.")

# 쿼리에 따라 텍스트를 검색하는 함수
def retrieve_documents(query, k=5):
    results = faiss.db.embeddings.embed_query(query)
    print(f"Retrieved {len(results)} document(s) for the query '{query}':")
    for doc, score in results:
        print(doc.metadata, doc.page_content, score)
    return results

# 특정 ID의 텍스트를 업데이트하는 함수
def update_text(id_to_update, new_text, new_metadata):
    faiss.db.delete_texts([id_to_update])
    faiss.db.add_texts([new_text], metadatas=[new_metadata], ids=[id_to_update])
    print(f"Updated document with ID: {id_to_update}")

# 특정 ID의 텍스트를 삭제하는 함수
def delete_text(ids):
    faiss.db.delete_texts(ids)
    print(f"Deleted document(s) with ID(s): {', '.join(ids)}")
from AI.db import faiss

# 데이터베이스에 새 텍스트를 추가하는 함수
def add_text(texts, metadatas, ids):
    ids, embed = faiss.db.add_texts(texts, metadatas=metadatas, ids=ids)
    print(f"Added {len(texts)} text(s) to the database.")
    faiss.save_db()
    return embed

# 쿼리에 따라 텍스트를 검색하는 함수
def retrieve_documents(query, ainame, k=4):
    # 예를 들어 results를 반환하는 함수를 가정하면,
    results = faiss.db.similarity_search(query, k, filter={"source": ainame})  # similarity_search 함수는 이미 정의되어 있다고 가정    
    return results


# 특정 ID의 텍스트를 업데이트하는 함수
def update_text(id_to_update, new_text, new_metadata):
    faiss.db.delete([id_to_update])
    faiss.db.add_texts([new_text], metadatas=[new_metadata], ids=[id_to_update])
    print(f"Updated document with ID: {id_to_update}")
    faiss.save_db()

# 특정 ID의 텍스트를 삭제하는 함수
def delete_text(ids):
    faiss.db.delete(ids)
    print(f"Deleted document(s) with ID(s): {', '.join(ids)}")
    faiss.save_db()
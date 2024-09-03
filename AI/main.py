from db import faiss
from crud import add_text


add_text(['In relationships between people, the most important thing is empathy. Through empathy, we can grow closer to one another. We naturally feel more drawn to those who show us genuine understanding.'], [{"source": "dating_adivce_ai"}], ['dating_advice_ai_1'])
print(faiss.db.index_to_docstore_id)

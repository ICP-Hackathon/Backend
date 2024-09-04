from AI.db import faiss
from AI.crud import retrieve_documents
from AI.llm import generate_answer

# add_text(["The pain of parting is often greater than the joy of meeting, so it's important to find the strength to overcome it."], [{"source": "dating_adivce_ai"}], ['dating_advice_ai_5'])
def rag_qa(question, ainame):
    retrieved_docs = retrieve_documents(question, ainame)
    response = generate_answer(question, retrieved_docs)
    tokens = response.usage
    answer = response.choices[0].message.content

    return tokens, answer
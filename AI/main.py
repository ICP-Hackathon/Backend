from db import faiss
from crud import retrieve_documents
from llm import generate_answer

# add_text(["The pain of parting is often greater than the joy of meeting, so it's important to find the strength to overcome it."], [{"source": "dating_adivce_ai"}], ['dating_advice_ai_5'])
def rag_qa(question):
    retrieved_docs = retrieve_documents(question)
    answer = generate_answer(question, retrieved_docs)
    return answer

# Example question
question = "What do you need to love?"
response = rag_qa(question)

tokens = response.usage
answer = response.choices[0].message.content

print("token usage")
print(tokens)

print("answer")
print(answer)
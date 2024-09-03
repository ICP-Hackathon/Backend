from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_community.chains import RetrievalQA
from langchain_community.llms import OpenAI
from AI.crud import retrieve_documents
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings()


template = """You are a helpful assistant. Use the following context to answer the question.

Context: {context}

Question: {question}

Answer:"""

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=template,
)

# 3. Set up the LLM (Large Language Model)
llm = OpenAI(model="gpt-3.5-turbo", temperature=0.7)


# 5. Function to generate an answer using the retrieved documents
def generate_answer(question, retrieved_docs):
    # Combine the content of the retrieved documents into a single context string
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    
    # Prepare the prompt with context and question
    final_prompt = prompt.format(context=context, question=question)
    
    # Generate the answer using the LLM
    answer = llm(final_prompt)
    return answer

# 6. Main process: Ask a question, retrieve documents, and generate an answer
question = "이번 텍스트 데이터에 포함된 내용이 무엇인가요?"
retrieved_docs = retrieve_documents(question)
answer = generate_answer(question, retrieved_docs)

# 7. Print the answer and the retrieved documents
print("Answer:", answer)
print("Retrieved Documents:")
for doc in retrieved_docs:
    print(doc.metadata, doc.page_content)
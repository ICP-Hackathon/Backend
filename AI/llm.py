from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from openai import OpenAI
import os

api_key = os.getenv('HYPERBOLIC_API_KEY')
load_dotenv()

client = OpenAI(
    api_key= api_key,
    base_url="https://api.hyperbolic.xyz/v1",
    )

embeddings = OpenAIEmbeddings()

template = """You are a helpful assistant that is an expert at extracting the most useful information from a given text.
 Also bring in extra relevant information to    the user query from outside the given context.
Context: {context}

Question: {question}

Answer:"""

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=template,
)

# 5. Function to generate an answer using the retrieved documents
def generate_answer(question, retrieved_docs):
    # Combine the content of the retrieved documents into a single context string
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    
    # Prepare the prompt with context and question
    final_prompt = prompt.format(context=context, question=question)
    print(final_prompt)
    # Using the chat completion endpoint for GPT-4
    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-70B-Instruct",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": final_prompt}
        ],
        temperature=0.7,
        max_tokens=128
    )
    return response
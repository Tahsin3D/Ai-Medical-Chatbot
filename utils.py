from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize a compatible embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")  # Fix: Use HuggingFaceEmbeddings

# Load an existing Pinecone index
doc_search = PineconeVectorStore.from_existing_index(
    index_name="medbot",  # Ensure this index exists in your Pinecone account
    embedding=embedding_model  # Fix: Use the correct embedding model
)


# Create a retriever
retriever = doc_search.as_retriever(search_type="similarity", search_kwargs={"k": 3})



from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.4,
    max_tokens=200,
    timeout=None,
    max_retries=3,
    google_api_key=GOOGLE_API_KEY
)



from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a medical companion to help people with their health-related queries. "
            "You answer based on retrieved context. If you don't find the answer from retrieved data, "
            "reply with 'I am sorry, I don't have the answer to that question.' "
            "at the end of each response ask casually if the user has any other questions."
            "Keep your response concise and under 100 words.\n\n"
            "Context:\n{context}"
        ),
        ("human", "{input}"),
    ]
)
chain = prompt | llm
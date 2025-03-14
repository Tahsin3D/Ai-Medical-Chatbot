# Description: This script stores the extracted text from a PDF file into a Pinecone index.
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from pinecone import Pinecone
import time
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore
from langchain.embeddings import SentenceTransformerEmbeddings

# Load the Pinecone API key from the .env file
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Path of the file to be indexed
file_path = "./Data/The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND.pdf"  # Relative path to the file

reader = PdfReader(file_path)


# Extract all the data from the file
extracted_text = ""
for page in reader.pages[:]:
    text = page.extract_text()
    if text:  # Check if text exists
        extracted_text += text + "\n\n"


# Splitting text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)
text_chunks = text_splitter.split_text(extracted_text)

# Load the SentenceTransformer model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Initialize a Pinecone client with your API key
pc = Pinecone(api_key=PINECONE_API_KEY)

# Define the index name
index_name = "medbot"

# Check if the index already exists
existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

# Create the index if it doesn't exist
if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)

# Connect to the index
index = pc.Index(index_name)

# Create a Pinecone Vector Store
vector_store = PineconeVectorStore(index=index, embedding=model)

# Convert text chunks into Document objects
documents = [Document(page_content=text) for text in text_chunks]

# Initialize LangChain's SentenceTransformer wrapper
embedding_model = SentenceTransformerEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create Pinecone Vector Store and automatically add documents
vector_store = PineconeVectorStore.from_documents(
    documents=documents,
    index_name="medbot",
    embedding=embedding_model
)

print("Documents successfully added to the Pinecone index.")
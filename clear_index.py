# Only use it to delete vectors
from pinecone import Pinecone
from dotenv import load_dotenv
import os

# Load the environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Define your index name
index_name = "medbot"

# Connect to the index
index = pc.Index(index_name)

# Delete all vectors
index.delete(delete_all=True)

print("All vectors have been deleted from the index.")
from utils import retriever, chain
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

async def process_query(user_query):
    retrieved_docs = retriever.invoke(user_query)
    return chain.invoke({"input": user_query, "context": retrieved_docs}).content

# Root Route
@app.get("/")
async def root():
    return {"message": "AI Medical Chatbot is running!"}

# Define input model
class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    chatbot_response = await process_query(request.query)
    return {"response": chatbot_response}





# Test the function
# user_query = "smile?"
# response = get_response(user_query)
# print(response)




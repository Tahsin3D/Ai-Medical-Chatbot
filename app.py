from utils import retriever, chain
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

def get_response(user_query):
    retrieved_docs = retriever.invoke(user_query)
    return chain.invoke({"input": user_query, "context": retrieved_docs}).content


# Define input model
class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def get_response(request: QueryRequest):
    chatbot_response = get_response(request.query)
    return {"response": chatbot_response}





# Test the function
# user_query = "smile?"
# response = get_response(user_query)
# print(response)




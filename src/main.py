from fastapi import FastAPI
from .api import chat  # Added space after 'from.' for clarity

# Create the FastAPI app instance
app = FastAPI(
    title="LangChain Groq Chat API",
    description="A simple API to chat with a Groq-powered LLM using LangChain.",
    version="1.0.0"
)

# Include the chat router
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])

@app.get("/", tags=["Root"])
async def read_root():
    """
    Root endpoint to confirm the API is running.
    """
    return {"status": "API is running"}

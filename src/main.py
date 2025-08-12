from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from .api import chat

# Create the FastAPI app instance
app = FastAPI(
    title="LangChain Groq Chat API",
    description="A simple API to chat with a Groq-powered LLM using LangChain.",
    version="1.0.0"
)

# Include the chat router
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])

# Mount static files if you have CSS/JS files (optional)
# app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", tags=["Root"])
async def read_root():
    """
    Serve the chat interface HTML page.
    """
    # Get the directory where this file is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Look for the HTML file in the same directory
    html_file = os.path.join(current_dir, "chat.html")
    
    # If chat.html exists, serve it; otherwise return API status
    if os.path.exists(html_file):
        return FileResponse(html_file, media_type="text/html")
    else:
        return {"status": "API is running", "message": "Chat interface not found. Please add chat.html file."}

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {"status": "healthy"}
import os
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler

def get_langfuse_handler():
    """Initialize and return Langfuse callback handler if configured"""
    if all([
        os.getenv("LANGFUSE_PUBLIC_KEY"),
        os.getenv("LANGFUSE_SECRET_KEY"),
        os.getenv("LANGFUSE_HOST")
    ]):
        langfuse = Langfuse(
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            host=os.getenv("LANGFUSE_HOST")
        )
        return CallbackHandler()
    return None

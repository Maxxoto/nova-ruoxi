from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def get_nova_response(user_query: str, groq_api_key: str) -> str:
    """Process user query using Groq LLM and return response.

    Args:
        user_query: The user's input message
        groq_api_key: API key for Groq service

    Returns:
        The generated response from the LLM
    """
    # Initialize Groq LLM
    llm = ChatGroq(
        temperature=0.7, model_name="qwen/qwen3-32b", groq_api_key=groq_api_key
    )

    # Create prompt template
    prompt_template = ChatPromptTemplate.from_template(
        """You are Nova, a helpful AI assistant. Respond to the user's message.

        User: {input}
        Nova:"""
    )

    # Create processing chain
    chain = prompt_template | llm | StrOutputParser()

    # Get response
    return chain.invoke({"input": user_query})

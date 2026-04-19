import os
from openai import AsyncAzureOpenAI, AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

def get_async_client():
    """
    Returns async OpenAI client based on available environment variables.
    Supports both Azure OpenAI (enterprise/gateway) and standard OpenAI.

    Priority:
    1. Azure OpenAI if MY_LLM_ENDPOINT and MY_LLM_API_KEY are set
    2. Standard OpenAI if OPENAI_API_KEY is set
    """
    llm_api_key = os.getenv("MY_LLM_API_KEY")
    llm_endpoint = os.getenv("MY_LLM_ENDPOINT")
    llm_api_version = os.getenv("MY_LLM_API_VERSION", "2024-10-21")
    openai_key = os.getenv("OPENAI_API_KEY")

    if llm_api_key and llm_endpoint:
        # Using Azure OpenAI or custom gateway endpoint
        return AsyncAzureOpenAI(
            api_version=llm_api_version,
            azure_endpoint=llm_endpoint,
            api_key=llm_api_key
        )
    elif openai_key:
        # Using standard OpenAI
        return AsyncOpenAI(api_key=openai_key)
    else:
        raise ValueError(
            "No API credentials found. Please configure .env with either:\n"
            "  Option 1 (Azure/Gateway): MY_LLM_API_KEY + MY_LLM_ENDPOINT\n"
            "  Option 2 (Standard OpenAI): OPENAI_API_KEY"
        )

async_client = get_async_client()

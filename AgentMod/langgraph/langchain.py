import os

import dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA


dotenv.load_dotenv()

def getLLModel():
    ## 定义LLM
    chat = ChatNVIDIA(
        base_url=os.getenv("BASE_URL"),
        model=os.getenv("MODEL_NAME"),
        api_key=os.getenv("API_KEY"),
        max_completion_tokens=2048,
    )
    return chat

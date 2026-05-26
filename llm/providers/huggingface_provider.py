import os
from dotenv import load_dotenv
from llm.providers.base import BaseLLMProvider
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace


load_dotenv()


class HuggingFaceLLMProvider(BaseLLMProvider):


    def __init__(self):
        
        endpoint = HuggingFaceEndpoint(
            huggingfacehub_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN"),
            repo_id = os.getenv("REPO_ID", "Qwen/Qwen2.5-72B-Instruct"),
            temperature = os.getenv("TEMPERATURE", 0.5),
            max_new_tokens = os.getenv("MAX_NEW_TOKENS", 200)
        )

        self.llm = ChatHuggingFace(llm = endpoint)


    def get_llm(self):

        return self.llm
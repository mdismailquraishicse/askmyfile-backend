from core.config import settings
from llm.providers.base import BaseLLMProvider
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace



class HuggingFaceLLMProvider(BaseLLMProvider):


    def __init__(self):
        
        endpoint = HuggingFaceEndpoint(
            huggingfacehub_api_token = settings.HUGGINGFACEHUB_API_TOKEN,
            repo_id = settings.MODEL_NAME,
            temperature = settings.TEMPERATURE,
            top_k = settings.TOP_K,
            top_p = settings.TOP_P,
            max_new_tokens = settings.MAX_NEW_TOKENS
        )

        self.llm = ChatHuggingFace(llm = endpoint)


    def get_llm(self):

        return self.llm
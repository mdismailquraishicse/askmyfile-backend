from base import BaseLLMProvider
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace


class HuggingFaceLLMProvider(BaseLLMProvider):


    def __init__(self):
        
        endpoint = HuggingFaceEndpoint(
            huggingfacehub_api_token = None,
            repo_id = None,
            temperature = 0,
            max_new_tokens = 1024
        )

        self.llm = ChatHuggingFace(llm = endpoint)



    def get_llm(self):

        return self.llm
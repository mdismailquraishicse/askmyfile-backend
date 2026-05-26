from llm.providers.huggingface_provider import HuggingFaceLLMProvider




class LLMFactory:


    @staticmethod
    def create(provider:str):

        providers = {
            "hf" : HuggingFaceLLMProvider
        }

        if provider not in providers:
            raise ValueError(f"Unsupported provider: {provider}")
        
        return providers.get(provider)().get_llm()
from core.config import settings
from llm.factory import LLMFactory
from services.prompt import rag_prompt




class LLMService:


    def __init__(self):
        
        provider = settings.PROVIDER
        self.llm = LLMFactory.create(provider = provider)
        self.prompt = rag_prompt
        self.chain = self.prompt | self.llm
        self.history = []


    def generate(self, question:str, context:str):

        response = self.chain.invoke({
            "chat_history": self.history,
            "question": question,
            "context": context
        })
        return response.content
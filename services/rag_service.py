from services.llm_service import LLMService
from services.retrieval_service import RetrievalService



class RAGService:


    def __init__(self):
        
        self.retrieval = RetrievalService()
        self.llm = LLMService()


    def ask(self, query:str, collection_name:str):

        context = self.retrieval.get_context(query = query,
                                             collection_name = collection_name,
                                             k = 1)
        answer = self.llm.generate(
            question = query,
            context = context
        )
        return {
            "answer": answer,
            "context": context
        }
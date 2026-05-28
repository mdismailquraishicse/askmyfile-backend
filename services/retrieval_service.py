from core.config import settings
from db.qdrant_db import VectorDB
from services.embedding_service import EmbeddingService




class RetrievalService:


    def __init__(self):
        
        self.embedding_service = EmbeddingService()
        self.db = VectorDB(host = settings.QDRANT_HOST,
                           port = settings.QDRANT_PORT)


    def get_context(self, query:str, collection_name:str, k:int):

        embedding = self.embedding_service.embed_query(query = query)
        fetched_data = self.db.search_similar_docs(
            embedding = embedding,
            collection_name = collection_name,
            k = k
        )

        context = "\n\n".join(
            [data.payload.get("text") for data in fetched_data.points]
        )
        return context
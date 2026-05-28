from services.embedding_service import EmbeddingService
from db.qdrant_db import VectorDB




class IngestionService:


    def __init__(self):
        
        self.embedding_service = EmbeddingService()
        self.db = VectorDB()


    def ingest_file(self, path:str, collection_name:str):

        chunks = self.embedding_service.chunk_doc(path = path)
        text = [chunk.page_content for chunk in chunks]
        embeddings = self.embedding_service.embed_text(text = text)
        upserted = self.db.upsert_to_db(embeddings = embeddings,
                             payload = text,
                             collection_name = collection_name)
        print(f"data upserted successfully")
        return upserted
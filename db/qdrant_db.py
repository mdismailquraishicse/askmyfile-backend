from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.models import PointStruct, Distance, VectorParams


class AskMyFileDB:


    def __init__(self, host:str, port:int):
        
        self.client = QdrantClient(
            host = host,
            port = port
        )

        self.vector_config = VectorParams(
            size = 768,
            distance = Distance.DOT
        )


    def create_collection(self, collection_name:str):

        response = self.client.create_collection(
            collection_name = collection_name,
            vectors_config = self.vector_config
        )
        return response
    

    def delete_collection(self, collection_name:str):

        return self.client.delete_collection(collection_name = collection_name)
    

    def upsert_to_db(self, embeddings, payload, collection_name:str):

        for i in range(0, len(embeddings)):

            self.client.upsert(
                collection_name = collection_name,
                wait = True,
                points = [PointStruct(
                    id = i,
                    vector = embeddings[i],
                    payload = {"text" : payload[i]}
                )]
            )
        
        print(f"data upserted successfully")
        return True
    

    def search_similar_docs(self, embedding, collection_name:str, k:int):

        data = self.client.query_points(
            collection_name = collection_name,
            query = embedding,
            with_payload = True,
            limit = k
        )

        return data
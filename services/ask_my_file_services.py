from services.prompt import rag_prompt
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from llm.factory import LLMFactory

from db.qdrant_db import AskMyFileDB


ask_my_file_db = AskMyFileDB(host = "localhost", port = 6333)
K = 5
COLLECTION_NAME = "my_collection"
provider = "hf"

class AskMyFileService:


    def __init__(self):
        
        self.hf_embed = HuggingFaceEmbeddings()
        self.chat_history = []
        self.llm = LLMFactory.create(provider = provider)
        self.prompt = rag_prompt
        self.chain = self.prompt | self.llm


    def chunking(self, path:str, n_chunk:int = 1000, chunk_overlap:int = 100):

        loader = PyPDFLoader(path)
        splitter = RecursiveCharacterTextSplitter(
            chunk_size = n_chunk,
            chunk_overlap = chunk_overlap
        )

        documents = loader.load()
        chunks = splitter.split_documents(documents)
        print(f"Document breaked into chunks: {len(chunks)}")
        return chunks
    

    def doc2embedding(self, docs:list):

        embedded_docs = self.hf_embed.embed_documents(docs)
        return embedded_docs
    

    def upsert_embeddings_to_vector_db(self, path:str, collection_name:str):

        chunks = self.chunking(path = path, n_chunk = 1000, chunk_overlap = 100)
        chunk_contents = [chunk.page_content for chunk in chunks]
        embedded_chunks = self.doc2embedding(docs = chunk_contents)
        response = ask_my_file_db.upsert_to_db(embeddings = embedded_chunks, payload = chunk_contents, collection_name = collection_name)
        print(f"successfully upserted")

    
    def get_context(self, query:str, collection_name:str, k:int=5):

        embedding = self.hf_embed.embed_query(text = query)
        data = ask_my_file_db.search_similar_docs(embedding = embedding, k = k, collection_name = collection_name)
        context = "\n\n".join([payload.payload.get("text") for payload in data.points])
        return context


    def invoke_llm(self, query:str):

        context = self.get_context(query=query, collection_name = COLLECTION_NAME, k = K)
        response = self.chain.invoke({
            "chat_history": self.chat_history,
            "question": query,
            "context" : context
        })

        answer = response.content
        return {
            "answer": answer,
            "context": context
        }
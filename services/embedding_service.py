from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings




class EmbeddingService:


    def __init__(self):
        
        self.embedder = HuggingFaceEmbeddings()

    
    def chunk_doc(self, path:str, chunk_size:int = 500, overlap:int = 50):

        loader = PyPDFLoader(path)
        splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap = overlap
        )

        documents = loader.load()
        chunks = splitter.split_documents(documents = documents)
        print(f"Document breaked into {len(chunks)} chunks")
        return chunks
    

    def embed_text(self, text: list[str]):

        return self.embedder.embed_documents(text)
    

    def embed_query(self, query:str):

        return self.embedder.embed_query(query)
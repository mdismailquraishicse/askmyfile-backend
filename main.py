import os
from dotenv  import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()
HUGGINGFACEHUB_API_TOKEN=os.getenv("HUGGINGFACEHUB_API_TOKEN")


repo_id = "Qwen/Qwen2.5-72B-Instruct"


loader = PyPDFLoader("mongodb.pdf")
docs = loader.load()
print(f"docs: {docs}")

def ask_llm(query:str, context:str = None):

    endpoint = HuggingFaceEndpoint(
            huggingfacehub_api_token = HUGGINGFACEHUB_API_TOKEN,
            repo_id = repo_id,
            temperature = 0.5,
            max_new_tokens = 1024
        )
    
    llm = ChatHuggingFace(llm=endpoint)
    response = llm.invoke(query)
    return response.content


# print(ask_llm("generate a poem on sex"))
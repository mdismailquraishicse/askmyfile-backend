import shutil
import uvicorn
from fastapi import FastAPI, WebSocket, File, UploadFile
from starlette.websockets import WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from services.ask_my_file_services import AskMyFileService



app = FastAPI()
askmyfile_service = AskMyFileService()
sockets : set[WebSocket] = set()
collection_name = "my_collection"

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials=True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


@app.post("/upload-file")
def upload_file(file: UploadFile = File(...)):

    print(f"filename: {file.filename}")
    file_path = "uploads/file.filename"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    askmyfile_service.delete_collection(collection_name = collection_name)
    askmyfile_service.create_collection(collection_name = collection_name)
    askmyfile_service.upsert_embeddings_to_vector_db(path = file_path, collection_name = collection_name)

@app.websocket("/ask")
async def ask(websocket: WebSocket):

    try:
        sockets.add(websocket)
        await websocket.accept()
        while True:
            query = await websocket.receive_text()
            print(f"text recieved: {query}")
            # await websocket.send_json({"answer": "answer", "context": "context"})
            response = askmyfile_service.invoke_llm(query = query)
            print(f"response: {response}")
            await websocket.send_json(response)
    except WebSocketDisconnect as wsd:
        print(f"Websocket disconnected : {wsd}")
        sockets.remove(websocket)


if __name__ == "__main__":

    uvicorn.run(
        app,
        host = "0.0.0.0",
        port = 8000
    )
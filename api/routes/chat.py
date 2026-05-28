from core.logger import logger
from fastapi import WebSocket, APIRouter
from starlette.websockets import WebSocketDisconnect
from services.rag_service import RAGService



router = APIRouter(prefix = "/chat", tags = ["Chat"])
rag = RAGService()
sockets : set[WebSocket] = set()
collection_name = "my_collection"


@router.websocket("/ask")
async def ask(websocket: WebSocket):

    try:
        await websocket.accept()
        sockets.add(websocket)
        while True:
            query = await websocket.receive_text()
            logger.info(f"text received: {query}")
            # await websocket.send_json({"answer": "answer", "context": "context"})
            response = rag.ask(query = query, collection_name = collection_name)
            logger.info(f"response: {response}")
            await websocket.send_json(response)

    except WebSocketDisconnect as wsd:
        logger.error(f"Websocket disconnected : {wsd}")

    except Exception as e:
        logger.error(f"Error: {e}")

        await websocket.send_json({
            "error": str(e)
        })

    finally:
        sockets.discard(websocket)

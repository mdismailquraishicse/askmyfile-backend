import os
import shutil
from core.logger import logger
from fastapi import File, UploadFile, APIRouter
from services.ingestion_service import IngestionService


router = APIRouter(prefix = "/upload", tags = ["Upload"])
ingestion = IngestionService()
collection_name = "my_collection"


@router.post("/file")
def upload_file(file: UploadFile = File(...)):

    logger.info(f"filename: {file.filename}")
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ingestion.delete_collection(collection_name = collection_name)
    ingestion.create_collection(collection_name = collection_name)
    ingestion.ingest_file(path = file_path, collection_name = collection_name)
    return {
        "message": "file uploaded successfully",
        "filename": file.filename
    }

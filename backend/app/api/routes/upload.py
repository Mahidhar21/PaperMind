from fastapi import (
    APIRouter,
    UploadFile,
    File
)

from pathlib import Path

from app.services.vectorstore.build_vector_db import (
    build_vector_database
)

router = APIRouter()

UPLOAD_DIR = Path("uploads")

UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")

async def upload_pdf(
    file: UploadFile = File(...)
):

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as f:

        content = await file.read()

        f.write(content)

    vector_info = build_vector_database(
        str(file_path)
    )

    return {
        "filename": file.filename,
        "message": "PDF uploaded successfully",
        "vector_database": vector_info
    }
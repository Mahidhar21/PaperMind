from fastapi import APIRouter, HTTPException
from pathlib import Path

from app.services.pdf.extractor import extract_text_from_pdf
from app.services.pdf.chunker import chunk_text

router = APIRouter()

UPLOAD_DIR = Path("uploads")


@router.get("/extract/{filename}")
async def extract_pdf_text(filename: str):

    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    extracted_text = extract_text_from_pdf(str(file_path))

    chunks = chunk_text(extracted_text)

    return {
        "filename": filename,
        "total_chunks": len(chunks),
        "chunks": chunks
    }
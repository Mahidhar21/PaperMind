from fastapi import APIRouter, HTTPException
from pathlib import Path

from app.services.pdf.extractor import extract_text_from_pdf
from app.services.summarizer.paper_summarizer import (
    generate_paper_summary
)

router = APIRouter()

UPLOAD_DIR = Path("uploads")


@router.get("/summary/{filename}")
async def summarize_paper(filename: str):

    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    extracted_text = extract_text_from_pdf(
        str(file_path)
    )

    summary = generate_paper_summary(
        extracted_text
    )

    return {
        "filename": filename,
        "summary": summary
    }
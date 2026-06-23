import os
import tempfile
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.report_generator import generate_weekly_report_pdf

router = APIRouter()

@router.get("/download")
async def download_report(db: AsyncSession = Depends(get_db)):
    """
    Generates a PDF Weekly Battle Card from live DB data and streams it to the browser.
    """
    # Write to a named temp file the browser can download
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", prefix="intelgraphx_report_")
    tmp.close()

    await generate_weekly_report_pdf(db=db, filepath=tmp.name)

    return FileResponse(
        path=tmp.name,
        filename="IntelGraphX_Weekly_Battle_Card.pdf",
        media_type="application/pdf"
    )

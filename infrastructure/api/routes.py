from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.api.schemas import P12ProcessRequest, ProcessResponse
from app.application.services.file_service import P12ProcessorService
from app.infrastructure.adapters.repositories.database_repository import DatabaseFileRepository
from app.infrastructure.adapters.file_converter.p12_converter import P12Converter
from app.infrastructure.config.database import get_db

router = APIRouter()


@router.post("/p12/process", response_model=ProcessResponse)
async def process_p12_file(
        config_id: str = Form(...),
        file_name: str = Form(None),
        p12_file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db)
):
    # Read file content
    file_content = await p12_file.read()

    # Use uploaded filename if file_name not provided
    if not file_name:
        file_name = p12_file.filename

    # Create repository and service instances
    file_repository = DatabaseFileRepository(db)
    file_converter = P12Converter()

    # Create processor service
    processor_service = P12ProcessorService(file_repository, file_converter)

    # Process the file
    success, error_message = await processor_service.process_p12_file(
        file_content,
        file_name,
        config_id
    )

    if success:
        return ProcessResponse(
            success=True,
            message=f"P12 file {file_name} processed successfully"
        )
    else:
        raise HTTPException(
            status_code=500,
            detail=error_message or "Unknown error occurred"
        )
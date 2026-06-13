import os
from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends
)
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Document
from app.services.pdf_parser import (
    extract_pdf_text,
    extract_txt_text
)
from app.services.chunking import (
    fixed_chunking,
    recursive_chunking
)
from app.services.embedding import (
    generate_embeddings
)
from app.vectorstore.vector_db import (
    create_collection,
    store_chunks
)

router = APIRouter()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    chunk_strategy: str = Form(...),
    db: Session = Depends(get_db)
):
    # Save file
    file_path = f"uploads/{file.filename}"
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Extract text
    if file.filename.lower().endswith(".pdf"):
        text = extract_pdf_text(file_path)
    elif file.filename.lower().endswith(".txt"):
        text = extract_txt_text(file_path)
    else:
        return {"error": "Only pdf and txt allowed"}
    
    # Apply chunking
    if chunk_strategy == "fixed":
        chunks = fixed_chunking(text)
    elif chunk_strategy == "recursive":
        chunks = recursive_chunking(text)
    else:
        return {"error": "Invalid strategy"}
    
    # Generate embeddings
    embeddings = generate_embeddings(chunks)
    
    # Store vectors
    create_collection()
    store_chunks(
        chunks=chunks,
        embeddings=embeddings,
        filename=file.filename
    )
    
    # Save metadata
    document = Document(
        filename=file.filename,
        chunk_strategy=chunk_strategy
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    
    # Return response
    return {
        "document_id": document.id,
        "filename": document.filename,
        "chunks_created": len(chunks),
        "strategy": chunk_strategy
    }

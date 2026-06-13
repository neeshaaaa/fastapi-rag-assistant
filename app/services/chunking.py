# Two chunking strategies

# Fixed Chunking

from typing import List


def fixed_chunking(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50
) -> List[str]:

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(
            text[start:end]
        )

        start += chunk_size - overlap

    return chunks




# Recursive chunking


from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


def recursive_chunking(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50
) -> List[str]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    return splitter.split_text(text)
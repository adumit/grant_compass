from typing import List, Tuple, Dict, Union
import os

import docx
import PyPDF2
from bs4 import BeautifulSoup


FileName = str
Percentile = float
ChunkIdx = int
ChunkKey = Tuple[Percentile, ChunkIdx]
KeyedChunkedText = Dict[ChunkKey, str]


def parse_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    full_text = [paragraph.text for paragraph in doc.paragraphs]
    return "\n".join(full_text)


def parse_pdf(file_path: str) -> List[Tuple[int, str]]:
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfFileReader(file)
        pages_text = []
        for page in range(reader.numPages):
            page_text = reader.getPage(page).extractText()
            pages_text.append((page, page_text))
        return pages_text


def parse_txt(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()


def parse_html(file_path: str) -> str:
    with open(file_path, "r") as file:
        soup = BeautifulSoup(file, "html.parser")
        return soup.get_text()


def calculate_percentile(start_index: int, total_length: int) -> float:
    return round((start_index / total_length) * 100, 2)


def chunk_text(
    text: Union[str, List[Tuple[int, str]]], chunk_size: int, overlap: int, is_pdf: bool
) -> KeyedChunkedText:
    if is_pdf and isinstance(text, list):
        words = [word for page_number, page_text in text for word in page_text.split()]
    else:
        words = text.split()
    total_length = len(words)
    chunks = {}
    i = 0
    chunk_index = 0
    while i < len(words):
        chunk = " ".join(words[i : i + chunk_size])
        if is_pdf:
            # For PDFs, use page number and chunk index
            key = (chunk_index, chunk_index)
        else:
            # For other file types, use percentile through the document
            percentile = calculate_percentile(i, total_length)
            key = (percentile, chunk_index)
        chunks[key] = chunk
        i += chunk_size - overlap
        chunk_index += 1
    return chunks


def process_file(
    file_path: str, file_type: str, chunk_size: int, overlap: int
) -> KeyedChunkedText:
    if file_type == "docx":
        text = parse_docx(file_path)
        is_pdf = False
    elif file_type == "pdf":
        pages_text = parse_pdf(file_path)
        return chunk_text(pages_text, chunk_size, overlap, True)
    elif file_type == "txt":
        text = parse_txt(file_path)
        is_pdf = False
    elif file_type == "html":
        text = parse_html(file_path)
        is_pdf = False
    else:
        raise ValueError("Unsupported file type")

    return chunk_text(text, chunk_size, overlap, is_pdf)


def process_files(
    file_paths: List[str], chunk_size: int, overlap: int
) -> Dict[FileName, KeyedChunkedText]:
    chunks = {}
    for file_path in file_paths:
        file_type = file_path.split(".")[-1]
        chunks[os.path.basename(file_path)] = process_file(
            file_path, file_type, chunk_size, overlap
        )
    return chunks

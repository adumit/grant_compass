from typing import Union
import os

import docx
import pdftotext
from bs4 import BeautifulSoup
from backend.document_types import FileName, KeyedChunkedText


def parse_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    full_text = [paragraph.text for paragraph in doc.paragraphs]
    return "\n".join(full_text)


def parse_pdf(file_path: str) -> list[tuple[int, str]]:
    try:
        with open(file_path, "rb") as file:
            pdf = pdftotext.PDF(file)
        pages_text = []
        for page in range(len(pdf)):
            page_text = pdf[page]
            pages_text.append((page, page_text))
        return pages_text
    except Exception as e:
        print("Error reading PDF:", e)
        return []


def parse_txt(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()


def parse_html(file_path: str) -> str:
    with open(file_path, "r") as file:
        soup = BeautifulSoup(file, "html.parser")
        return soup.get_text()


def calculate_percentile(start_index: int, total_length: int) -> float:
    return round((start_index / total_length) * 100, 2)


def maybe_split_combined_chunk(chunk: str, chunk_size: int) -> list[str]:
    """

    This splits on char length, potentially cutting a word. This handles documents that have
    no spaces or newlines. This can happen when parsing different kinds
    of documents, primarily seen with PDFs. The models actaully understand the text without
    spaces fairly well, but this can lead to crazy-large chunks, which do break the API call

    """
    char_split_length = chunk_size * 5  # Assume rough average of 5 chars per word

    # Split if the number of characters is 6*number of words. Slight upper bound on the number
    if len(chunk) > chunk_size * 6:
        return [
            chunk[i * char_split_length : (i + 1) * char_split_length]
            for i in range(0, len(chunk) // char_split_length + 1)
        ]
    else:
        return [chunk]


def split_str(text: str) -> list[str]:
    return text.replace("\n", " ").split()


def chunk_text(
    text: Union[str, list[tuple[int, str]]], chunk_size: int, overlap: int, is_pdf: bool
) -> KeyedChunkedText:
    """
    chunk_size: number of words to include in each chunk
    overlap: number of words to overlap between chunks
    """
    if is_pdf and isinstance(text, list):
        # TODO: Alternative way of handling PDFs.. to be tested.
        # Might be more confusing to have two different handlings of documents though.
        # chunks_across_pages = {}
        # for page_number, page_text in text:
        #     chunks_from_page = chunk_text(page_text, chunk_size, overlap, is_pdf)
        #     for chunk_key, chunk in chunks_from_page.items():
        #         chunks_across_pages[(page_number, chunk_key[1])] = chunk
        # return chunks_across_pages
        words = [
            word for page_number, page_text in text for word in split_str(page_text)
        ]
        total_length = sum([len(page_text) for _, page_text in text])
    else:
        words = split_str(text)
        total_length = len(text)

    chunks = {}
    raw_chunks = [
        subchunk
        for chunk in [
            " ".join(words[i : i + chunk_size])
            for i in range(0, len(words), chunk_size)
        ]
        for subchunk in maybe_split_combined_chunk(chunk, chunk_size)
        if len(chunk) > 0 and len(subchunk) > 0
    ]
    current_text_covered = 0
    for chunk_idx, chunk in enumerate(raw_chunks):
        percentile = calculate_percentile(current_text_covered, total_length)
        key = (percentile, chunk_idx)
        chunks[key] = chunk
        current_text_covered += len(chunk) - (overlap * 5)  # Roughly 5 chars per word
    return chunks


def chunk_single_file(
    file_path: str, file_type: str, chunk_size: int, overlap: int
) -> KeyedChunkedText:
    if file_type == "docx":
        text = parse_docx(file_path)
        is_pdf = False
    elif file_type == "pdf":
        pages_text = parse_pdf(file_path)
        if not pages_text:
            raise ValueError(f"Could not parse PDF {file_path}")
        return chunk_text(pages_text, chunk_size, overlap, True)
    elif file_type == "txt":
        text = parse_txt(file_path)
        is_pdf = False
    elif file_type == "html":
        text = parse_html(file_path)
        is_pdf = False
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

    return chunk_text(text, chunk_size, overlap, is_pdf)


def chunk_files(
    file_paths: list[str], chunk_size: int, overlap: int
) -> dict[FileName, KeyedChunkedText]:
    chunks = {}
    for file_path in file_paths:
        file_type = file_path.split(".")[-1]
        try:
            chunks[os.path.basename(file_path)] = chunk_single_file(
                file_path, file_type, chunk_size, overlap
            )
        except ValueError:
            print(f"Skipping file {file_path} due to unsupported file type")
            continue
    return chunks

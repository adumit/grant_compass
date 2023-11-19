import argparse
import json
import os

from backend.parse_documents import chunk_files
from backend.document_types import (
    KeyedChunkedText,
    FileName,
    EmbeddedRelatedDocumentChunks,
)
from backend.embed import embed_chunks

from .pull_gov_grants_zip_files import pull_gov_grants_zip_files
from .unzip_grant_files import unzip_and_map_files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download zip files for current grants"
    )
    parser.add_argument(
        "--download_path", type=str, help="Path to check for complete downloads"
    )
    parser.add_argument(
        "--n_grants",
        type=int,
        default=-1,
        help="Number of grants to download, -1 for all",
    )
    parser.add_argument(
        "--chunk_size", type=int, default=500, help="Number of words per chunk"
    )
    parser.add_argument(
        "--overlap", type=int, default=100, help="Number of words to overlap"
    )

    args = parser.parse_args()
    if args.download_path:
        DOWNLOAD_PATH = args.download_path
    if args.n_grants:
        n_grants = args.n_grants

    # First download all of the needed files
    opportunity_id_to_zips = pull_gov_grants_zip_files(
        args.download_path, args.n_grants
    )

    # Then unzip the files
    print("Unzipping files")
    opportunity_id_to_files = unzip_and_map_files(
        args.download_path, opportunity_id_to_zips
    )

    print("Chunking files")
    opportunity_id_to_fname_with_chunked_text: dict[
        str, dict[FileName, KeyedChunkedText]
    ] = {}
    # Then for each file, chunk and embed with the appropriate mapping
    for opportunity_id, files in opportunity_id_to_files.items():
        fname_to_chunks: dict[FileName, KeyedChunkedText] = chunk_files(
            files, chunk_size=args.chunk_size, overlap=args.overlap
        )
        opportunity_id_to_fname_with_chunked_text[opportunity_id] = fname_to_chunks

    print("Embedding chunks")
    # Then for each chunk, embed with the appropriate mapping and save them to disk for now
    # TODO: Maybe upload them directly to AWS bucket or write them to a DB?
    for (
        opportunity_id,
        file_name_to_chunks,
    ) in opportunity_id_to_fname_with_chunked_text.items():
        embedded_chunks = embed_chunks(file_name_to_chunks)
        jsonifiable_data_stucture: dict[str, EmbeddedRelatedDocumentChunks] = {}
        for (file_name, chunk_key), (chunk_embedding, chunk) in embedded_chunks.items():
            jsonifiable_data_stucture[f"{file_name}-{chunk_key[0]}-{chunk_key[1]}"] = {
                "embedding": chunk_embedding,
                "opportunity_id": opportunity_id,
                "file_name": file_name,
                "chunk_key": chunk_key,
                "chunk": chunk,
            }
        with open(
            os.path.join(
                os.path.dirname(__file__),
                "embedded_document_results",
                f"{opportunity_id}-embedded-related-document-chunks.json",
            ),
            "w",
        ) as f:
            json.dump(jsonifiable_data_stucture, f)

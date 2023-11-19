from typing import TypedDict


FileName = str
Percentile = float
ChunkIdx = int
ChunkKey = tuple[Percentile, ChunkIdx]
KeyedChunkedText = dict[ChunkKey, str]
TextEmbedding = list[float]
KeyedChunkedTextWithEmbeddings = dict[
    tuple[FileName, ChunkKey], tuple[TextEmbedding, str]
]


class EmbeddedRelatedDocumentChunks(TypedDict):
    opportunity_id: int
    file_name: FileName
    chunk_key: ChunkKey
    chunk: str
    embedding: TextEmbedding

FileName = str
Percentile = float
ChunkIdx = int
ChunkKey = tuple[Percentile, ChunkIdx]
KeyedChunkedText = dict[ChunkKey, str]
TextEmbedding = list[float]
KeyedChunkedTextWithEmbeddings = dict[tuple[FileName, ChunkKey], TextEmbedding]

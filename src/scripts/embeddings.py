from pathlib import Path
import json
from sentence_transformers import SentenceTransformer
import numpy as np

def load_chunks(chunks_dir: Path) -> list[dict]:
    """
    Carrega todos os chunks dos arquivos JSONL.
    """

    chunks = []

    for jsonl_path in chunks_dir.glob("*.jsonl"):
        print(f"Carregando: {jsonl_path.name}")

        with jsonl_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                if not line:
                    continue

                chunk = json.loads(line)
                chunks.append(chunk)

    return chunks

def gerarEmbeddings(modelo, chunks_dir: Path, embeddings_dir):
    model = SentenceTransformer(modelo)

    # Carrega todos os chunks dos JSONL
    chunks = load_chunks(chunks_dir)

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True,
        batch_size=32,
    )

    np.save(
        embeddings_dir,
        embeddings
    )

def consultarEmbeddings(modelo, embeddings_path: str, chunks, query: str, k: int = 5):
    model = SentenceTransformer(modelo)
    embeddings = np.load(embeddings_path)

    query_embedding = model.encode(
        query,
        normalize_embeddings=True,
    )

    scores = embeddings @ query_embedding
    indices = np.argsort(scores)[::-1][:k]

    results = []
    
    for idx in indices:
        chunk = chunks[idx].copy()
        chunk["score"] = float(scores[idx])
        results.append(chunk)
    
    return results

from pathlib import Path
import json
import re
import unicodedata

from rank_bm25 import BM25Okapi

def normalize_text(text: str) -> str:
    """
    Normaliza o texto para busca BM25.

    - converte para minúsculas
    - remove acentos
    - mantém apenas palavras/números
    """
    text = text.lower()

    # Remove acentos
    text = unicodedata.normalize("NFKD", text)
    text = "".join(
        char
        for char in text
        if not unicodedata.combining(char)
    )

    return text


def tokenize(text: str) -> list[str]:
    """
    Converte um texto em tokens para o BM25.
    """
    text = normalize_text(text)

    return re.findall(r"\b\w+\b", text)


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


def build_bm25(chunks: list[dict]):
    """
    Cria o índice BM25 a partir dos chunks.
    """

    corpus = [
        tokenize(chunk["text"])
        for chunk in chunks
    ]

    return BM25Okapi(corpus)


def searchBM25(
    bm25,
    chunks: list[dict],
    query: str,
    top_k: int = 5,
):
    """
    Executa uma busca BM25 e retorna os chunks mais relevantes.
    """

    query_tokens = tokenize(query)

    scores = bm25.get_scores(query_tokens)

    # Índices ordenados pela maior pontuação
    ranked_indexes = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True,
    )

    results = []

    for index in ranked_indexes[:top_k]:
        chunk = chunks[index].copy()
        chunk["score"] = float(scores[index])

        results.append(chunk)

    return results

def carregarBM25(chunks_dir):
    
    # 1. Carrega todos os chunks
    chunks = load_chunks(chunks_dir)

    # 2. Cria índice BM25
    bm25 = build_bm25(chunks)

    return bm25, chunks
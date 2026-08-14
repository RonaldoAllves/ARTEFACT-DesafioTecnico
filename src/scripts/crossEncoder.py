from scripts.bm25 import searchBM25, carregarBM25
from scripts.fusion import Rrf
from scripts.rerank import rerank
from scripts.embeddings import consultarEmbeddings
from sentence_transformers import CrossEncoder

def crossEncoder(chunks_dir, query, modelo, modelo_rerank, embeddings_dir, k=5, top_k=1):
    bm25, chunks = carregarBM25(chunks_dir)
    bm25_results = searchBM25(bm25, chunks, query, k)
    embedding_results = consultarEmbeddings(modelo, embeddings_dir, chunks, query, k)

    rrf_results = Rrf(
        [
            embedding_results,
            bm25_results,
        ]
    )

    reranker = CrossEncoder(modelo_rerank)

    final_results = rerank(
        reranker,
        query,
        rrf_results[:10],
        top_k,
    )

    return final_results

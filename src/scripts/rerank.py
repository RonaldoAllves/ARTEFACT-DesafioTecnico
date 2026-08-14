def rerank(
    reranker,
    query: str,
    documents: list[dict],
    top_k: int = 5,
):
    """
    Reordena os documentos utilizando Cross Encoder.
    """

    pairs = [
        (query, doc["text"])
        for doc in documents
    ]

    scores = reranker.predict(pairs)

    results = []

    for doc, score in zip(documents, scores):

        item = doc.copy()
        item["rerank_score"] = float(score)

        results.append(item)

    results.sort(
        key=lambda x: x["rerank_score"],
        reverse=True,
    )

    return results[:top_k]
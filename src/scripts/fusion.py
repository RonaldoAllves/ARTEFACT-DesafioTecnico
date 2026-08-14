from collections import defaultdict

def Rrf(
    rankings,
    k=60,
):
    scores = defaultdict(float)
    documents = {}

    for ranking in rankings:

        for rank, doc in enumerate(ranking, start=1):

            key = (
                doc["chunk_id"],
            )

            documents[key] = doc

            scores[key] += 1 / (k + rank)

    fused = []

    for key, score in scores.items():

        doc = documents[key].copy()
        doc["rrf_score"] = score

        fused.append(doc)

    fused.sort(
        key=lambda x: x["rrf_score"],
        reverse=True,
    )

    return fused
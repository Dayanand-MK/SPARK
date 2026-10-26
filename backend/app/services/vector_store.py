from functools import lru_cache
from pathlib import Path
from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from app.config import settings

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
QDRANT_PATH = str(Path(__file__).resolve().parents[2] / "qdrant_data")


@lru_cache(maxsize=1)
def get_embedding_model():
    return SentenceTransformer(MODEL_NAME)


@lru_cache(maxsize=1)
def get_qdrant_client():
    return QdrantClient(path=QDRANT_PATH)


def ensure_collection():
    client = get_qdrant_client()
    collection = settings.qdrant_collection

    if not client.collection_exists(collection):
        client.create_collection(
            collection_name=collection,
            vectors_config=models.VectorParams(
                size=384,
                distance=models.Distance.COSINE,
            ),
        )


def index_papers(papers: list[dict]) -> int:
    if not papers:
        return 0

    ensure_collection()
    model = get_embedding_model()
    client = get_qdrant_client()

    texts = [
        f"{paper['title']}. {paper['abstract']}"
        for paper in papers
    ]
    vectors = model.encode(texts, normalize_embeddings=True)

    import uuid

    points = []
    for paper, vector in zip(papers, vectors):
        point_id = str(uuid.uuid5(uuid.NAMESPACE_URL, paper["url"]))
        points.append(
            models.PointStruct(
                id=point_id,
                vector=vector.tolist(),
                payload=paper,
            )
        )

    client.upsert(
        collection_name=settings.qdrant_collection,
        points=points,
        wait=True,
    )
    return len(points)


def semantic_search(query: str, limit: int = 5) -> list[dict]:
    ensure_collection()
    model = get_embedding_model()
    client = get_qdrant_client()

    vector = model.encode(
        query,
        normalize_embeddings=True,
    ).tolist()

    result = client.query_points(
        collection_name=settings.qdrant_collection,
        query=vector,
        limit=limit,
        with_payload=True,
    )

    return [
        {"score": hit.score, **(hit.payload or {})}
        for hit in result.points
    ]
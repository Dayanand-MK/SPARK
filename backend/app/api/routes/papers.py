from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.paper_search import search_arxiv
from app.services.vector_store import index_papers, semantic_search

router = APIRouter()


class PaperSearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=200)
    limit: int = Field(default=10, ge=1, le=20)


@router.post("/search")
async def search_papers(request: PaperSearchRequest):
    try:
        papers = await search_arxiv(
            query=request.query,
            limit=request.limit,
        )
    except Exception as exc:
        # Log the actual exception in a production application.
        raise HTTPException(
            status_code=502,
            detail="The external paper search service failed. Please retry.",
        ) from exc

    return {
        "query": request.query,
        "source": "arXiv",
        "total": len(papers),
        "papers": papers,
    }


@router.get("/status")
def paper_search_status():
    return {
        "service": "paper-search",
        "status": "ready",
    }

class SemanticSearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=500)
    limit: int = Field(default=5, ge=1, le=20)


@router.post("/index")
async def index_search_results(request: PaperSearchRequest):
    try:
        papers = await search_arxiv(
            query=request.query,
            limit=request.limit,
        )
        count = index_papers(papers)

        return {
            "query": request.query,
            "papers_found": len(papers),
            "papers_indexed": count,
            "vector_database": "Qdrant",
        }
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="Paper indexing failed. Check the paper API, embedding model and Qdrant.",
        ) from exc


@router.post("/semantic-search")
def search_similar_papers(request: SemanticSearchRequest):
    try:
        results = semantic_search(
            request.query,
            request.limit,
        )
        return {
            "query": request.query,
            "total": len(results),
            "results": results,
        }
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Semantic search failed. Check the embedding model and Qdrant.",
        ) from exc

import httpx
import xml.etree.ElementTree as ET


ARXIV_API_URL = "https://export.arxiv.org/api/query"

ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}


async def search_arxiv(query: str, limit: int = 10) -> list[dict]:
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": limit,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(ARXIV_API_URL, params=params)
        response.raise_for_status()

    root = ET.fromstring(response.text)
    papers = []

    for entry in root.findall("atom:entry", ATOM_NS):
        authors = [
            author.findtext("atom:name", default="", namespaces=ATOM_NS)
            for author in entry.findall("atom:author", ATOM_NS)
        ]

        papers.append({
            "paper_id": (
                entry.findtext("atom:id", default="", namespaces=ATOM_NS)
                .rstrip("/")
                .split("/")[-1]
            ),
            "title": " ".join(
                entry.findtext(
                    "atom:title", default="", namespaces=ATOM_NS
                ).split()
            ),
            "authors": authors,
            "abstract": " ".join(
                entry.findtext(
                    "atom:summary", default="", namespaces=ATOM_NS
                ).split()
            ),
            "published": entry.findtext(
                "atom:published", default="", namespaces=ATOM_NS
            ),
            "url": entry.findtext(
                "atom:id", default="", namespaces=ATOM_NS
            ),
            "source": "arXiv",
        })

    return papers

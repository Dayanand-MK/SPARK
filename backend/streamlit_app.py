
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="SPARK | Research Discovery",
    page_icon="🔬",
    layout="wide",
)

st.title("🔬 SPARK")
st.subheader("Scientific Paper Analysis & Research Knowledge Discovery")
st.write(
    "Explore scientific literature using semantic search "
    "and AI-powered paper retrieval."
)

with st.form("research_form"):
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Plant disease detection using deep learning",
    )

    limit = st.slider(
        "Number of papers to retrieve",
        min_value=1,
        max_value=10,
        value=5,
    )

    submitted = st.form_submit_button(
        "Find and analyze papers",
        type="primary",
    )

if submitted:
    if len(topic.strip()) < 2:
        st.warning("Please enter a research topic.")
    else:
        try:
            with st.spinner(
                "Searching scientific papers and creating embeddings..."
            ):
                index_response = requests.post(
                    f"{API_URL}/papers/index",
                    json={"query": topic.strip(), "limit": limit},
                    timeout=180,
                )
                index_response.raise_for_status()
                index_data = index_response.json()

            st.success("Paper indexing completed!")

            col1, col2 = st.columns(2)
            col1.metric(
                "Papers found",
                index_data.get("papers_found", 0),
            )
            col2.metric(
                "Papers indexed",
                index_data.get("papers_indexed", 0),
            )

            with st.spinner("Finding semantically similar papers..."):
                search_response = requests.post(
                    f"{API_URL}/papers/semantic-search",
                    json={"query": topic.strip(), "limit": limit},
                    timeout=180,
                )
                search_response.raise_for_status()
                search_data = search_response.json()

            st.subheader("Research papers")
            results = search_data.get("results", [])

            if not results:
                st.info(
                    "No indexed papers were returned. "
                    "Try another research topic."
                )

            for i, paper in enumerate(results, start=1):
                title = paper.get("title") or "Untitled paper"

                with st.container(border=True):
                    st.markdown(f"### {i}. {title}")

                    authors = paper.get("authors", [])
                    if isinstance(authors, list):
                        authors = ", ".join(authors)

                    if authors:
                        st.caption(f"Authors: {authors}")

                    published = paper.get("published")
                    if published:
                        st.caption(f"Published: {published[:10]}")

                    score = paper.get("score")
                    if score is not None:
                        st.caption(
                            f"Semantic similarity score: {score:.3f}"
                        )

                    abstract = paper.get("abstract", "")
                    if abstract:
                        with st.expander("Read abstract"):
                            st.write(abstract)

                    url = paper.get("url")
                    if url:
                        st.markdown(f"[Read original paper]({url})")

            st.caption(
                "Similarity scores indicate embedding similarity, "
                "not research quality or confidence."
            )

        except requests.RequestException as exc:
            st.error(
                "Could not communicate with the SPARK API. "
                "Check that FastAPI is running at "
                "http://127.0.0.1:8000."
            )
            st.code(str(exc))

        except (ValueError, TypeError, KeyError) as exc:
            st.error(f"Could not process the API response: {exc}")

st.divider()
st.caption("SPARK MVP · FastAPI · arXiv · Sentence Transformers · Qdrant")

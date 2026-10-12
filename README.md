# Agentic RAG — NCERT Geography Assistant

End-to-end **agentic RAG** capstone: index a geography PDF in Chroma, expose retrieval as a tool, and run a **ReAct-style** agent (OpenAI-compatible API via OpenRouter) with optional Streamlit UI.

## Architecture

```
geography.pdf → rag.py → Chroma (collection: geography)
                              ↑
User question → agent.py → LLM decides tool → search_geography → chunks → LLM answer
```

## Basic vs optimized

| Version | Folder | Tool returns | Who synthesizes the answer |
|---------|--------|--------------|----------------------------|
| **Basic** | repo root (`tools.py`) | LLM answer from chunks | LLM inside the tool (~double LLM use) |
| **Optimized** | `optimized_version/` | Raw chunk text only | Agent LLM once (`MAX_STEPS=3`, `n_results=4`) |

## Setup

```bash
cd agentic-rag-geography
pip install -r requirements.txt
cp .env.example .env
# Set OPENROUTER_API_KEY
python rag.py
```

Index runs only when the collection is empty (`collection.count() == 0`).

## Run

**CLI (basic):**

```bash
python agent.py
```

**CLI (optimized):**

```bash
cd optimized_version
python agent.py
```

**Streamlit (basic):**

```bash
streamlit run streamlit_app.py
```

**Streamlit (optimized):**

```bash
cd optimized_version
streamlit run streamlit_app.py
```

## Manual evaluation (summary)

Three test questions were used to compare retrieval and faithfulness (e.g. strong cases: Thar Desert, Aravallis; weaker case when the book lacks detail for the query). Tuning notes: increasing `n_results` reduced redundant tool rounds; `MAX_STEPS` caps the ReAct loop.

## Interview highlights

- Built **tool calling** and **ReAct loop** from scratch (no agent framework).
- **Optimized** pipeline: single synthesis at the agent, retrieval-only tool.
- **Chroma** + **Chonkie** chunking on real PDF text.

## Data

`geography.pdf` is used for educational demo (NCERT-style geography). Replace with your own PDF and re-run `rag.py` for other domains.

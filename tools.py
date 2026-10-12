import os
from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI
import chromadb

client = chromadb.PersistentClient(path="./chromadb")
collection = client.get_or_create_collection(name="geography")


def search_geography(query:str) -> str:
    
    result = collection.query(
        query_texts = [query],
        n_results = 2

    )

    top_chunks = result["documents"][0]

    context = ""
    for chunk in top_chunks:
        context = context + chunk + "\n\n"

    load_dotenv(Path(__file__).resolve().parent / ".env")    
    llm_client = OpenAI(
        base_url = "https://openrouter.ai/api/v1",
        api_key = os.getenv("OPENROUTER_API_KEY")
    )

    prompt = f"""Answer the question using the context only. do not assume anything on your own.
    If not in context, say "I don't know."
    context : {context}

    Question: {query}

    """

    llm_response = llm_client.chat.completions.create(
        model= "openrouter/free",
        messages = [{"role": "user", "content": prompt}]
    )

    return llm_response.choices[0].message.content

import chromadb

client = chromadb.PersistentClient(path="../chromadb")
collection = client.get_or_create_collection(name="geography")


def search_geography(query:str) -> str:
    
    result = collection.query(
        query_texts = [query],
        n_results = 4

    )

    top_chunks = result["documents"][0]

    context = ""
    for chunk in top_chunks:
        context = context + chunk + "\n\n"

    return context   

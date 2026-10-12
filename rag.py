from pypdf import PdfReader
from pathlib import Path
from chonkie import TokenChunker
import chromadb
from openai import OpenAI
import os
from dotenv import load_dotenv

"""
steps for pdf extraction and making chunks of the extracted text
"""
path = "./geography.pdf"
reader = PdfReader(path)
text = ""
for page in reader.pages:
    text = text + page.extract_text()

chunker = TokenChunker(
    tokenizer = "character",
    chunk_size = 500,
    chunk_overlap = 300,
)
chunks = chunker.chunk(text)
texts = []
for c in chunks:
    texts.append(c.text) 

ids = []
for i in range(len(chunks)):
    ids.append("doc_" + str(i))

"""
Steps for adding the chunks into chromadb
"""
client = chromadb.PersistentClient(path = "./chromadb")

collection = client.get_or_create_collection(name = "geography")

if collection.count() == 0:

    collection.add(
        ids = ids,
        documents= texts
    )

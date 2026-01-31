from fastapi import FastAPI
from models import MessageIn
from extraction import normalize_text, extract_fields
from embedding import create_embedding
from vector_store import add_vector, search_vector

app = FastAPI()


@app.post("/message/ingest")
def ingest(msg: MessageIn):
    # 1. Clean WhatsApp text
    clean = normalize_text(msg.message_text)

    # 2. Extract fields (pass original message to preserve emoji markers)
    fields = extract_fields(msg.message_text)

    # 3. Create embedding (backend only)
    embedding = create_embedding(clean)

    # 4. Store in vector DB
    add_vector(embedding, fields)

    # 5. Return JSON only
    return {
        "raw_message": msg.message_text,
        "description": clean,
        "extracted_fields": fields,
        "LOCATION":fields.get('location')
    }


@app.post("/search")
def search(query: str):
    embedding = create_embedding(query)
    return search_vector(embedding)

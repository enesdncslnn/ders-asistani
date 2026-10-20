import chromadb
import ollama

EMBED_MODEL = "bge-m3"
DB_PATH = "data/chroma"
COLLECTION_NAME = "ders_notlari"


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Metin listesini Ollama üzerinden embedding vektörlerine çevirir."""
    try:
        response = ollama.embed(model=EMBED_MODEL, input=texts)
    except ConnectionError as e:
        raise RuntimeError(
            "Ollama'ya bağlanılamadı. Ollama uygulamasının çalıştığından emin ol."
        ) from e
    except ollama.ResponseError as e:
        raise RuntimeError(
            f"Embedding hatası: {e}. Model indirilmiş mi? (ollama pull {EMBED_MODEL})"
        ) from e
    return response["embeddings"]


def get_collection():
    """Diskte saklanan ChromaDB koleksiyonunu açar (yoksa oluşturur)."""
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},  # benzerlik ölçüsü: kosinüs
    )


def build_index(chunks: list[dict], batch_size: int = 32) -> int:
    """Chunk'ları embedding'leyip ChromaDB'ye kaydeder. Kaydedilen sayıyı döndürür."""
    collection = get_collection()
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        collection.upsert(  # upsert: aynı id varsa günceller, tekrar çalıştırmak güvenli
            ids=[c["id"] for c in batch],
            documents=[c["text"] for c in batch],
            embeddings=embed_texts([c["text"] for c in batch]),
            metadatas=[{"page": c["page"]} for c in batch],
        )
    return collection.count()


def search(question: str, top_k: int = 3) -> list[dict]:
    """Soruya en yakın chunk'ları döndürür: {'id', 'page', 'text', 'distance'}."""
    collection = get_collection()
    result = collection.query(
        query_embeddings=embed_texts([question]),
        n_results=top_k,
    )
    hits = []
    for i in range(len(result["ids"][0])):
        hits.append(
            {
                "id": result["ids"][0][i],
                "page": result["metadatas"][0][i]["page"],
                "text": result["documents"][0][i],
                "distance": result["distances"][0][i],  # küçük = daha yakın
            }
        )
    return hits
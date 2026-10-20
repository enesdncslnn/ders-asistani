from pathlib import Path

from src.chunker import chunk_pages
from src.pdf_loader import extract_pages


def test_chunking():
    pdfs = list(Path("data/pdfs").glob("*.pdf"))
    assert pdfs, "data/pdfs klasöründe PDF yok."

    pages = extract_pages(str(pdfs[0]))
    chunks = chunk_pages(pages, chunk_size=800, overlap=150)

    lengths = [len(c["text"]) for c in chunks]
    print("Sayfa sayısı:", len(pages))
    print("Chunk sayısı:", len(chunks))
    print("En kısa / en uzun chunk:", min(lengths), "/", max(lengths))
    print("Örnek chunk:", chunks[3]["id"], "(sayfa", chunks[3]["page"], ")")
    print(chunks[3]["text"])

    assert len(chunks) >= len(pages)
    assert max(lengths) <= 800
    assert all("page" in c and "id" in c for c in chunks)


if __name__ == "__main__":
    test_chunking()
    print("TEST GEÇTİ: Chunking çalışıyor.")
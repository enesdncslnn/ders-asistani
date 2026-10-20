from pathlib import Path

from src.chunker import chunk_pages
from src.pdf_loader import extract_pages
from src.vector_store import build_index, search


def test_index_and_search():
    pdfs = list(Path("data/pdfs").glob("*.pdf"))
    assert pdfs, "data/pdfs klasöründe PDF yok."

    chunks = chunk_pages(extract_pages(str(pdfs[0])))
    total = build_index(chunks)
    print("Veritabanındaki chunk sayısı:", total)
    assert total == len(chunks)

    question = "Çanakkale savaşında ne oldu?"
    hits = search(question, top_k=3)

    print("\nSoru:", question)
    for h in hits:
        print(f"\n--- {h['id']} | sayfa {h['page']} | uzaklık {h['distance']:.3f}")
        print(h["text"][:250])

    assert len(hits) == 3
    assert any("anakkale" in h["text"] for h in hits)


if __name__ == "__main__":
    test_index_and_search()
    print("\nTEST GEÇTİ: İndeksleme ve arama çalışıyor.")
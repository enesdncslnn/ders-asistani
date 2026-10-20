from pathlib import Path

from src.pdf_loader import extract_pages


def test_extract_pages():
    pdfs = list(Path("data/pdfs").glob("*.pdf"))
    assert pdfs, "data/pdfs klasöründe PDF yok. Bir ders PDF'i kopyala."

    pages = extract_pages(str(pdfs[0]))
    total_chars = sum(len(p["text"]) for p in pages)

    print("Dosya:", pdfs[0].name)
    print("Metin içeren sayfa sayısı:", len(pages))
    print("Toplam karakter:", total_chars)
    print("İlk sayfanın ilk 300 karakteri:")
    print(pages[0]["text"][:300])

    assert total_chars > 100


if __name__ == "__main__":
    test_extract_pages()
    print("TEST GEÇTİ: PDF metni çıkarıldı.")
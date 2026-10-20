from pathlib import Path

import pymupdf as fitz  # PyMuPDF

def extract_pages(pdf_path: str) -> list[dict]:
    """PDF'teki her sayfanın metnini {'page': sayfa_no, 'text': metin} olarak döndürür."""
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF bulunamadı: {path}")

    pages = []
    with fitz.open(path) as doc:
        for index, page in enumerate(doc, start=1):  # sayfa numarası 1'den başlar
            text = page.get_text().strip()
            if text:  # boş sayfaları atla
                pages.append({"page": index, "text": text})

    if not pages:
        raise ValueError(
            "PDF'ten metin çıkarılamadı. Dosya taranmış bir görüntü olabilir (OCR gerekir)."
        )
    return pages
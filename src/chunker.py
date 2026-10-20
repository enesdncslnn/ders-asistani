def chunk_pages(
    pages: list[dict], chunk_size: int = 800, overlap: int = 150
) -> list[dict]:
    """Sayfa metinlerini karakter bazlı, örtüşmeli parçalara böler.

    Her parça: {'id': 'sayfa-parça', 'page': sayfa_no, 'text': metin}
    """
    if overlap >= chunk_size:
        raise ValueError("overlap, chunk_size'dan küçük olmalı.")

    chunks = []
    step = chunk_size - overlap

    for page in pages:
        text = page["text"]
        part = 0
        for start in range(0, len(text), step):
            piece = text[start : start + chunk_size].strip()
            if len(piece) < 50:  # çok kısa artık parçaları atla
                continue
            part += 1
            chunks.append(
                {
                    "id": f"p{page['page']}_c{part}",
                    "page": page["page"],
                    "text": piece,
                }
            )
    return chunks
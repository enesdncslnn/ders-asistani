# Ders Asistanı (RAG)

Ders PDF'lerinden soru yanıtlayan, tamamen yerel ve ücretsiz çalışan RAG prototipi.

## Gereksinimler
- Python 3.11
- [Ollama](https://ollama.com/download) (uygulama arka planda açık olmalı)

## Kurulum
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
ollama pull qwen2.5:7b
ollama pull bge-m3
```
İlk model indirmeleri toplam yaklaşık 6 GB, sadece bir kez internet gerekir.

## Kullanım
1. Bir ders PDF'ini `data/pdfs/` klasörüne koy.
2. Testleri çalıştır (ilki indeksi oluşturur): `python -m tests.test_vector_store`
3. Soru sor: `python ask.py`

## Yapı
- `src/pdf_loader.py`: PDF'ten sayfa sayfa metin
- `src/chunker.py`: metni parçalara bölme
- `src/vector_store.py`: embedding + ChromaDB + arama
- `src/llm_client.py`: Ollama LLM bağlantısı
- `src/rag.py`: kaynağa dayalı cevap üretme
- `tests/`: her aşama için küçük testler
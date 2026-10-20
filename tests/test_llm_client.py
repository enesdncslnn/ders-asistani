from src.llm_client import ask_llm


def test_llm_responds():
    answer = ask_llm("2 + 2 kaçtır? Sadece sayıyı yaz.")
    print("Model cevabı:", answer)
    assert "4" in answer


if __name__ == "__main__":
    test_llm_responds()
    print("TEST GEÇTİ: LLM bağlantısı çalışıyor.")
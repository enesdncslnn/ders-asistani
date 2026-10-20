from src.rag import answer_question

QUESTIONS = [
    "Çanakkale savaşında ne oldu?",         # kaynakta var
    "Kut'ül Amare'de ne oldu?",             # kaynakta var
    "Python'da liste nasıl sıralanır?",     # kaynakta YOK (ders dışı)
    "Fransız İhtilali ne zaman başladı?",   # konu yakın ama kaynakta olmayabilir
]


def test_rag():
    for q in QUESTIONS:
        result = answer_question(q)
        print("=" * 70)
        print("SORU:", q)
        print("CEVAP:", result["answer"])
        print("Kaynak bulundu mu:", result["found"])
        print(
            "Kaynaklar:",
            [(s["page"], round(s["distance"], 3)) for s in result["sources"]],
        )


if __name__ == "__main__":
    test_rag()
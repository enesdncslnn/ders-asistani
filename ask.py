from src.rag import answer_question


def main():
    print("Ders asistanı hazır. Çıkmak için boş bırakıp Enter'a bas.\n")
    while True:
        question = input("Soru: ").strip()
        if not question:
            break

        result = answer_question(question)
        print("\nCevap:", result["answer"])

        if result["found"]:
            print("\nDayandığı kaynaklar:")
            for s in result["sources"]:
                preview = s["text"][:120].replace("\n", " ")
                print(f"  - Sayfa {s['page']} (uzaklık {s['distance']:.3f}): {preview}...")
        print()


if __name__ == "__main__":
    main()
import ollama

MODEL_NAME = "qwen2.5:7b"


def ask_llm(prompt: str, model: str = MODEL_NAME) -> str:
    """Ollama'daki yerel modele bir istem gönderir ve metin cevabını döndürür."""
    try:
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0.1, "num_ctx": 8192},
            )
    except ConnectionError as e:
        raise RuntimeError(
            "Ollama'ya bağlanılamadı. Ollama uygulamasının çalıştığından emin ol."
        ) from e
    except ollama.ResponseError as e:
        raise RuntimeError(
            f"Ollama hata döndürdü: {e}. Model indirilmiş mi? (ollama pull {model})"
        ) from e

    return response["message"]["content"]
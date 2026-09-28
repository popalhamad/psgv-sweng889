import os
import time
import requests

from langchain_ollama import ChatOllama


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")


def wait_for_ollama():
    print("Waiting for Ollama to start...")

    for _ in range(30):
        try:
            response = requests.get(f"{OLLAMA_URL}/api/tags")
            if response.status_code == 200:
                print("Ollama is running.")
                return
        except requests.exceptions.ConnectionError:
            pass

        time.sleep(2)

    raise RuntimeError("Ollama did not start in time.")


def pull_model():
    print(f"Pulling model: {MODEL}")

    response = requests.post(
        f"{OLLAMA_URL}/api/pull",
        json={"model": MODEL},
        stream=True,
    )

    if response.status_code != 200:
        raise RuntimeError(f"Failed to pull model: {response.text}")

    for line in response.iter_lines():
        if line:
            print(line.decode("utf-8"))

    print("Model is ready.")


def create_llm():
    return ChatOllama(
        model=MODEL,
        base_url=OLLAMA_URL,
        temperature=0,
    )


def setup_llm():
    wait_for_ollama()
    pull_model()
    return create_llm()

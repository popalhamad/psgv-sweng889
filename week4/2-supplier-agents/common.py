"""Shared helpers: the connection to the local LLM, and small console utilities.

You should not need to change this file for the assignment.
"""

import os
import sys
import time

import requests
from langchain_ollama import ChatOllama

MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")


def get_llm(temperature: float = 0.0) -> ChatOllama:
    """The reasoning component shared by both agents."""
    return ChatOllama(model=MODEL, base_url=OLLAMA_URL, temperature=temperature)


def ask(llm: ChatOllama, prompt: str) -> str:
    """One call to the model. Returns plain text."""
    return llm.invoke(prompt).content.strip()


def banner(title: str) -> None:
    """Prints a stage marker so you can follow the workflow in the console.

    The sequence of banners in one run is a trace of the interaction between
    the user, the two agents, and the tool. Useful evidence for your UML
    sequence diagram.
    """
    print("\n" + "=" * 68)
    print(f"  {title}")
    print("=" * 68)


def ensure_model() -> None:
    """Waits for the Ollama container and downloads the model on first run."""
    deadline = time.time() + 120
    tags = None
    while time.time() < deadline:
        try:
            response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
            if response.ok:
                tags = response.json()
                break
        except requests.RequestException:
            pass
        print("Waiting for the Ollama container ...")
        time.sleep(3)

    if tags is None:
        sys.exit(
            f"Could not reach Ollama at {OLLAMA_URL}.\n"
            "Start it first with:  docker compose up -d ollama"
        )

    installed = [m.get("name", "") for m in tags.get("models", [])]
    if MODEL in installed:
        return

    print(f"Downloading model {MODEL}. The first run can take a few minutes ...")
    with requests.post(
        f"{OLLAMA_URL}/api/pull", json={"model": MODEL}, stream=True, timeout=1800
    ) as response:
        if not response.ok:
            sys.exit(f"Could not download {MODEL}: {response.text}")
        for line in response.iter_lines():
            if line:
                print(".", end="", flush=True)
    print(f"\nModel {MODEL} is ready.")

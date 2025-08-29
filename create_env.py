import os
from pathlib import Path


TEMPLATE = """# Which LLM to use: OpenAI or Ollama
LLM_PROVIDER=OpenAI

# OpenAI
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3:8b-instruct

# Model behavior
AI_TEMPERATURE=0.2
"""


def write_file(path: Path, content: str):
    path.write_text(content, encoding="utf-8")
    print(f"Wrote {path}")


def main():
    root = Path(__file__).resolve().parent
    env_example = root / ".env.example"
    env_file = root / ".env"

    if not env_example.exists():
        write_file(env_example, TEMPLATE)
    else:
        print(f"Exists: {env_example}")

    if not env_file.exists():
        write_file(env_file, TEMPLATE)
    else:
        print(f"Exists: {env_file}")


if __name__ == "__main__":
    main()



from pathlib import Path

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

from common import setup_llm


DATA_FILE = Path("data/course_policy.txt")


@tool
def read_course_policy() -> str:
    """Read the local SWENG 889 course policy file."""
    if not DATA_FILE.exists():
        return "The course policy file was not found."

    return DATA_FILE.read_text()


def main():
    llm = setup_llm()

    question = "According to the course policy file, what does Module 4 introduce?"

    print("\nQuestion:")
    print(question)

    print("\nAgent step 1: reading the local file...")
    tool_result = read_course_policy.invoke({})
    print(tool_result)

    print("\nAgent step 2: asking the local LLM to answer using the file content...")

    prompt = f"""
You are a helpful course assistant.

Answer the question using only the course policy content below.

Question:
{question}

Course policy content:
{tool_result}

Write one short sentence.
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    print("\nFinal agent response:")
    print(response.content)


if __name__ == "__main__":
    main()

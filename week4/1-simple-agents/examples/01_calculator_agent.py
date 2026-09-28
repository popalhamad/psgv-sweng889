from langchain.agents import create_agent
from langchain_core.tools import tool

from common import setup_llm


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers and return the result."""
    return a * b


def main():
    llm = setup_llm()

    agent = create_agent(
        model=llm,
        tools=[multiply],
        system_prompt=(
            "You are a helpful calculator assistant. "
            "Use the available tool for multiplication. "
            "Answer briefly."
        ),
    )

    prompt = "What is 18.5 multiplied by 4? Use the tool."

    print("\nPrompt:")
    print(prompt)

    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )

    print("\nAgent response:")
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()

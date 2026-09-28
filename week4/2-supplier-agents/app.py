"""Supplier selection — a small multi-agent system.

    Factory user
        -> Buyer Agent                  (identifies criteria, coordinates)
            -> Supplier Analysis Agent  (compares options, recommends)
                -> Supplier Information Tool
        -> Factory user                 (final answer)

Run with:  docker compose run --rm agent-app
"""

from agents.buyer_agent import handle_request
from common import MODEL, ensure_model, get_llm
from tools.supplier_tool import supplier_information

DEFAULT_REQUEST = (
    "The factory needs 400 units within 7 days. "
    "Recommend the best supplier and explain the decision."
)

MENU = """
Supplier selection multi-agent system   (model: {model})

  1. Run the default factory request
  2. Enter your own factory request
  3. Show the supplier catalogue (tool output only)
  q. Quit
"""


def main() -> None:
    ensure_model()
    llm = get_llm()

    while True:
        print(MENU.format(model=MODEL))
        choice = input("Choose an option: ").strip().lower()

        if choice == "1":
            handle_request(llm, DEFAULT_REQUEST)
        elif choice == "2":
            request = input("\nFactory request: ").strip()
            if request:
                handle_request(llm, request)
        elif choice == "3":
            print("\n" + supplier_information.invoke({}))
        elif choice == "q":
            print("Goodbye.")
            return
        else:
            print("Please choose 1, 2, 3, or q.")


if __name__ == "__main__":
    main()

import subprocess
import sys


EXAMPLES = {
    "1": {
        "name": "Calculator Agent",
        "file": "examples/01_calculator_agent.py",
    },
    "2": {
        "name": "Local File Reader Agent",
        "file": "examples/02_local_file_reader_agent.py",
    },
}


def show_menu():
    print("\n==============================")
    print(" Module 4: Simple Agents")
    print("==============================")
    print("Choose an example to run:\n")

    for key, example in EXAMPLES.items():
        print(f"{key}. {example['name']}")

    print("q. Quit")


def run_example(example_file):
    print("\nRunning example...")
    print("------------------------------")

    result = subprocess.run(
        [sys.executable, example_file],
        text=True,
    )

    print("------------------------------")

    if result.returncode != 0:
        print("The example finished with an error.")
    else:
        print("Example finished successfully.")


def main():
    while True:
        show_menu()
        choice = input("\nEnter your choice: ").strip().lower()

        if choice == "q":
            print("Goodbye!")
            break

        if choice not in EXAMPLES:
            print("Invalid choice. Please try again.")
            continue

        run_example(EXAMPLES[choice]["file"])

        input("\nPress Enter to return to the menu...")


if __name__ == "__main__":
    main()

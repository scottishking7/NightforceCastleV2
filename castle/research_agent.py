from castle.research_sources import trusted_sources
from castle.research_engine import run_research, search_documentation


def research_agent():

    while True:

        print()
        print("🔎 RESEARCH AGENT")
        print("-----------------")
        print()
        print("1 - Midnight Research")
        print("2 - Trusted Sources")
        print("3 - Saved Research")
        print("4 - Documentation Search")
        print("5 - Return")
        print()

        choice = input("Choose: ")

        print()

        if choice == "1":

            midnight_research()

        elif choice == "2":

            show_trusted_sources()

        elif choice == "3":

            print("🚧 Saved Research coming soon!")
            input("\nPress Enter to continue...")

        elif choice == "4":

            documentation_search()

        elif choice == "5":

            return

        else:

            print("❌ Invalid choice.")
            input("\nPress Enter to continue...")


def midnight_research():

    print()
    print("=" * 70)
    print("MIDNIGHT RESEARCH")
    print("=" * 70)
    print()

    question = input(
        "What would you like Castle to research? "
    ).strip()

    if not question:

        print()
        print("No research question entered.")
        input("\nPress Enter to continue...")
        return

    print()
    print("Choose Research Source")
    print()

    for key, source in trusted_sources.items():

        print(f"{key} - {source['name']}")

    print()

    source_choice = input("Choose: ")

    source = trusted_sources.get(source_choice)

    if not source:

        print()
        print("❌ Invalid source selection.")
        input("\nPress Enter to continue...")
        return

    print()
    print("Research request prepared...")
    print()

    print("QUESTION:")
    print(question)
    print()

    print("SOURCE:")
    print(source["name"])
    print(source["url"])
    print()

    result = run_research(
        question,
        source["name"],
        source["url"]
    )

    print("STATUS:")
    print(result["status"])
    print()

    input("Press Enter to continue...")


def documentation_search():

    print()
    print("=" * 70)
    print("DOCUMENTATION SEARCH")
    print("=" * 70)
    print()

    documentation = """
Selective disclosure allows users to prove information
without revealing unnecessary private information.

Zero knowledge proofs allow a user to prove something
without revealing the underlying secret information.

Midnight provides privacy-preserving smart contracts.

Compact is the smart contract language used by Midnight.

Midnight is designed to provide programmable privacy.

Privacy can allow users to control what information
they reveal and to whom they reveal it.
"""

    question = input(
        "Search documentation for: "
    ).strip()

    if not question:

        print()
        print("No search entered.")
        input("\nPress Enter to continue...")
        return

    results = search_documentation(
        documentation,
        question
    )

    print()
    print("SEARCH RESULTS")
    print("=" * 70)
    print()

    if not results:

        print("No matching documentation found.")

    else:

        for number, result in enumerate(results, start=1):

            print(
                f"{number}. {result['entry']}"
            )

            print(
                f"   Score: {result['score']}"
            )

            print()

    input("Press Enter to continue...")


def show_trusted_sources():

    print()
    print("=" * 70)
    print("TRUSTED SOURCES")
    print("=" * 70)
    print()

    for key, source in trusted_sources.items():

        print(f"{key} - {source['name']}")
        print(f"    {source['url']}")
        print()

    input("Press Enter to continue...")
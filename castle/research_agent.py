
from castle.research_sources import trusted_sources
from castle.research_engine import (
    run_research,
    search_documentation,
    build_research_result,
    load_cached_source
)


RESEARCH_VAULT = "research_vault.txt"
MIDNIGHT_CACHE = "midnight_docs.txt"


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

            saved_research()

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

    cached = load_cached_source(
        MIDNIGHT_CACHE
    )

    if cached["status"] != "SUCCESS":

        print(
            "Castle could not find the local Midnight documentation cache."
        )

        print()
        print(
            "Cache status:"
        )

        print(
            cached["status"]
        )

        print()
        print(
            cached["message"]
        )

        print()
        print(
            "The documentation must be cached before it can be searched."
        )

        input("\nPress Enter to continue...")
        return

    print(
        "Local Midnight documentation loaded."
    )

    print()

    question = input(
        "Search documentation for: "
    ).strip()

    if not question:

        print()
        print("No search entered.")
        input("\nPress Enter to continue...")
        return

    results = search_documentation(
        cached["content"],
        question
    )

    research_result = build_research_result(
        question,
        "Midnight Documentation",
        "https://docs.midnight.network",
        results
    )

    print()
    print("=" * 70)
    print("RESEARCH RESULT")
    print("=" * 70)
    print()

    print("QUESTION")
    print(research_result["question"])
    print()

    print("SOURCE")
    print(research_result["source"])
    print(research_result["url"])
    print()

    print("TRUSTED SOURCE")
    print(
        "YES ✓"
        if research_result["trusted"]
        else "NO ✗"
    )

    print()

    print("STATUS")
    print(research_result["status"])
    print()

    print("CACHE")
    print("LOCAL COPY")
    print()

    print("RELEVANT INFORMATION")
    print("-" * 70)

    if not research_result["results"]:

        print("No matching documentation found.")

    else:

        for number, result in enumerate(
            research_result["results"],
            start=1
        ):

            print()
            print(
                f"{number}. {result['entry']}"
            )

            print()
            print(
                f"   Relevance Score: {result['score']}"
            )

    print()
    print("-" * 70)

    if research_result["results"]:

        print()

        save = input(
            "Save this research to the Research Vault? (y/n): "
        ).strip().lower()

        if save == "y":

            save_research(
                research_result
            )

    input("\nPress Enter to continue...")


def save_research(research_result):

    with open(
        RESEARCH_VAULT,
        "a",
        encoding="utf-8"
    ) as file:

        file.write("\n")
        file.write("=" * 70 + "\n")
        file.write("NIGHTFORCE CASTLE RESEARCH\n")
        file.write("=" * 70 + "\n")

        file.write(
            f"QUESTION: {research_result['question']}\n"
        )

        file.write(
            f"SOURCE: {research_result['source']}\n"
        )

        file.write(
            f"URL: {research_result['url']}\n"
        )

        file.write(
            f"TRUSTED: {research_result['trusted']}\n"
        )

        file.write(
            f"STATUS: {research_result['status']}\n"
        )

        file.write(
            "CACHE: LOCAL COPY\n"
        )

        file.write(
            "\nRELEVANT INFORMATION:\n"
        )

        file.write(
            "-" * 70 + "\n"
        )

        for number, result in enumerate(
            research_result["results"],
            start=1
        ):

            file.write(
                f"{number}. {result['entry']}\n"
            )

            file.write(
                f"   Relevance Score: {result['score']}\n"
            )

        file.write(
            "=" * 70 + "\n"
        )

    print()
    print(
        "✅ Research saved to the Research Vault."
    )


def saved_research():

    print()
    print("=" * 70)
    print("SAVED RESEARCH")
    print("=" * 70)
    print()

    try:

        with open(
            RESEARCH_VAULT,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

        if not content.strip():

            print("No saved research yet.")

        else:

            print(content)

    except FileNotFoundError:

        print("No saved research yet.")

        print()

        print(
            "Research will appear here after you save"
        )

        print(
            "your first research result."
        )

    input("\nPress Enter to continue...")


def show_trusted_sources():

    print()
    print("=" * 70)
    print("TRUSTED SOURCES")
    print("=" * 70)
    print()

    for key, source in trusted_sources.items():

        print(
            f"{key} - {source['name']}"
        )

        print(
            f"    {source['url']}"
        )

        print()

    input(
        "Press Enter to continue..."
    )
from castle.research_sources import trusted_sources

from castle.research_engine import (
    run_research,
    search_documentation,
    build_research_result,
    load_cached_source,
    cache_source,
    get_cache_metadata,
    parse_research_vault,
    search_research_history
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
        print("5 - Cache Manager")
        print("6 - Return")
        print()

        choice = input("Choose: ").strip()

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

            cache_manager()

        elif choice == "6":

            return

        else:

            print("Invalid choice.")
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

    print("1 - Midnight Network")
    print("2 - Midnight Documentation")
    print("3 - Midnight Documentation Index")
    print("4 - Cardano")
    print("5 - Return")
    print()

    source_choice = input(
        "Choose: "
    ).strip()

    if source_choice == "5":

        return

    if source_choice == "1":

        source = trusted_sources.get("1")

    elif source_choice == "2":

        source = trusted_sources.get("2")

    elif source_choice == "3":

        source = trusted_sources.get("2")

    elif source_choice == "4":

        source = trusted_sources.get("3")

    else:

        print()
        print("Invalid source selection.")
        input("\nPress Enter to continue...")
        return

    if not source:

        print()
        print("Selected trusted source is unavailable.")
        input("\nPress Enter to continue...")
        return

    print()

    if source_choice in ("2", "3"):

        research_from_cache(
            question,
            source
        )

        return

    result = run_research(
        question,
        source["name"],
        source["url"]
    )

    print()
    print("QUESTION:")
    print(question)
    print()

    print("SOURCE:")
    print(source["name"])
    print(source["url"])
    print()

    print("STATUS:")
    print(result["status"])
    print()

    print(
        "This source is currently configured "
        "for trusted-source research."
    )

    input("\nPress Enter to continue...")


def research_from_cache(
    question,
    source
):

    cached = load_cached_source(
        MIDNIGHT_CACHE
    )

    if cached["status"] != "SUCCESS":

        print()
        print("CACHE STATUS:")
        print(cached["status"])
        print()

        print(cached["message"])
        print()

        print(
            "Castle could not perform the research "
            "from the local cache."
        )

        input("\nPress Enter to continue...")
        return

    results = search_documentation(
        cached["content"],
        question
    )

    result = build_research_result(
        question,
        source["name"],
        source["url"],
        results,
        cached.get(
            "cache_file",
            str(
                "castle/research_cache/"
                + MIDNIGHT_CACHE
            )
        )
    )

    display_research_report(
        result
    )

    if result["results"]:

        print()

        save_choice = input(
            "Save this research to the Research Vault? (y/n): "
        ).strip().lower()

        if save_choice == "y":

            save_research(
                result
            )

    input("\nPress Enter to continue...")


def classify_evidence(
    item
):

    concepts = item.get(
        "matched_concepts",
        []
    )

    score = item.get(
        "score",
        0
    )

    if score >= 3:

        return "PRIMARY EVIDENCE"

    if concepts:

        return "RELATED EVIDENCE"

    return "CONTEXT"


def display_research_report(
    result
):

    print()
    print("=" * 70)
    print("RESEARCH REPORT")
    print("=" * 70)
    print()

    print("QUESTION:")
    print(result["question"])
    print()

    print("SOURCE:")
    print(result["source"])
    print(result["url"])
    print()

    print("TRUSTED:")
    print(
        "YES ✓"
        if result["trusted"]
        else "NO ✗"
    )
    print()

    print("STATUS:")
    print(result["status"])
    print()

    print("KEY FINDINGS:")
    print("-" * 70)

    if not result["results"]:

        print()
        print(
            "No matching information found "
            "in the local documentation."
        )

        print()
        print("-" * 70)

        return

    evidence_counts = {
        "PRIMARY EVIDENCE": 0,
        "RELATED EVIDENCE": 0,
        "CONTEXT": 0
    }

    for item in result["results"]:

        evidence_type = classify_evidence(
            item
        )

        evidence_counts[
            evidence_type
        ] += 1

        print()
        print(
            f"{item.get('evidence_id', 'E???')} "
            f"{evidence_type}"
        )

        print(
            f"   {item['entry']}"
        )

        print(
            f"   Relevance Score: "
            f"{item['score']}"
        )

        if item.get("matched_words"):

            print(
                "   Matched Terms: "
                + ", ".join(
                    item["matched_words"]
                )
            )

        if item.get("matched_concepts"):

            print(
                "   Matched Concepts: "
                + ", ".join(
                    item["matched_concepts"]
                )
            )

        provenance = item.get(
            "provenance",
            {}
        )

        print(
            "   Source Line: "
            + str(
                provenance.get(
                    "cache_line",
                    item.get(
                        "line_number",
                        "Unknown"
                    )
                )
            )
        )

        print(
            "   Cache: "
            + str(
                provenance.get(
                    "cache_file",
                    result.get(
                        "cache_file",
                        "Unknown"
                    )
                )
            )
        )

    print()
    print("-" * 70)

    print()
    print("REPORT SUMMARY:")

    print(
        f"{len(result['results'])} "
        "relevant evidence entries found."
    )

    print(
        "Primary Evidence: "
        + str(
            evidence_counts[
                "PRIMARY EVIDENCE"
            ]
        )
    )

    print(
        "Related Evidence: "
        + str(
            evidence_counts[
                "RELATED EVIDENCE"
            ]
        )
    )

    print(
        "Context: "
        + str(
            evidence_counts[
                "CONTEXT"
            ]
        )
    )


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
            "No local Midnight documentation "
            "cache is available."
        )

        print()
        print(cached["message"])

        input("\nPress Enter to continue...")
        return

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

    print()
    print("SEARCH RESULTS")
    print("=" * 70)
    print()

    if not results:

        print(
            "No matching documentation found."
        )

    else:

        for result in results:

            print(
                f"{result.get('evidence_id', 'E???')}. "
                f"{result['entry']}"
            )

            print(
                f"   Line: "
                f"{result.get('line_number', 'Unknown')}"
            )

            print(
                f"   Score: "
                f"{result['score']}"
            )

            if result.get("matched_words"):

                print(
                    "   Matched Terms: "
                    + ", ".join(
                        result["matched_words"]
                    )
                )

            if result.get("matched_concepts"):

                print(
                    "   Matched Concepts: "
                    + ", ".join(
                        result["matched_concepts"]
                    )
                )

            print()

    input("Press Enter to continue...")


def cache_manager():

    while True:

        print()
        print("=" * 70)
        print("CACHE MANAGER")
        print("=" * 70)
        print()

        print(
            "1 - Cache Midnight Documentation"
        )

        print(
            "2 - Check Cache Status"
        )

        print(
            "3 - Return"
        )

        print()

        choice = input(
            "Choose: "
        ).strip()

        print()

        if choice == "1":

            cache_midnight_documentation()

        elif choice == "2":

            cache_status()

        elif choice == "3":

            return

        else:

            print("Invalid choice.")
            input("\nPress Enter to continue...")


def cache_midnight_documentation():

    print()
    print("=" * 70)
    print("CACHE MIDNIGHT DOCUMENTATION")
    print("=" * 70)
    print()

    source = trusted_sources.get(
        "2"
    )

    if not source:

        print(
            "Midnight Documentation source is unavailable."
        )

        input("\nPress Enter to continue...")
        return

    print("SOURCE:")
    print(source["name"])
    print(source["url"])
    print()

    print(
        "Castle will attempt to retrieve "
        "the trusted documentation."
    )

    print()

    result = cache_source(
        source["url"],
        MIDNIGHT_CACHE
    )

    print("STATUS:")
    print(result["status"])
    print()

    print(result["message"])

    if result.get("cache_file"):

        print()
        print("CACHE FILE:")
        print(result["cache_file"])

    input("\nPress Enter to continue...")


def cache_status():

    print()
    print("=" * 70)
    print("CACHE STATUS")
    print("=" * 70)
    print()

    cached = load_cached_source(
        MIDNIGHT_CACHE
    )

    metadata_result = get_cache_metadata(
        MIDNIGHT_CACHE
    )

    print("STATUS:")
    print(cached["status"])
    print()

    print(cached["message"])
    print()

    if cached["status"] == "SUCCESS":

        metadata = metadata_result.get(
            "metadata",
            {}
        )

        print(
            "DOCUMENTATION AVAILABLE:"
        )

        print(
            "YES ✓"
        )

        print()

        print(
            "CACHE FILE:"
        )

        print(
            metadata.get(
                "cache_file",
                cached.get(
                    "cache_file",
                    MIDNIGHT_CACHE
                )
            )
        )

        print()

        print(
            "SIZE:"
        )

        print(
            f"{metadata.get('size_bytes', 0)} bytes"
        )

        print()

        print(
            "LAST UPDATED:"
        )

        print(
            metadata.get(
                "updated_at",
                "Unknown"
            )
        )

        print()

        print(
            "METADATA STATUS:"
        )

        print(
            metadata_result["status"]
        )

    else:

        print(
            "DOCUMENTATION AVAILABLE:"
        )

        print(
            "NO ✗"
        )

    input("\nPress Enter to continue...")


def save_research(
    research_result
):

    with open(
        RESEARCH_VAULT,
        "a",
        encoding="utf-8"
    ) as file:

        file.write("\n")
        file.write(
            "=" * 70
            + "\n"
        )

        file.write(
            "NIGHTFORCE CASTLE RESEARCH\n"
        )

        file.write(
            "=" * 70
            + "\n"
        )

        file.write(
            f"QUESTION: "
            f"{research_result['question']}\n"
        )

        file.write(
            f"SOURCE: "
            f"{research_result['source']}\n"
        )

        file.write(
            f"URL: "
            f"{research_result['url']}\n"
        )

        file.write(
            f"TRUSTED: "
            f"{research_result['trusted']}\n"
        )

        file.write(
            f"STATUS: "
            f"{research_result['status']}\n"
        )

        file.write(
            "CACHE: LOCAL COPY\n"
        )

        file.write(
            "\nEVIDENCE:\n"
        )

        file.write(
            "-" * 70
            + "\n"
        )

        for result in (
            research_result["results"]
        ):

            evidence_type = classify_evidence(
                result
            )

            provenance = result.get(
                "provenance",
                {}
            )

            file.write(
                f"{result.get('evidence_id', 'E???')} "
                f"{evidence_type}\n"
            )

            file.write(
                f"   Evidence: "
                f"{result['entry']}\n"
            )

            file.write(
                f"   Relevance Score: "
                f"{result['score']}\n"
            )

            file.write(
                f"   Source Line: "
                f"{provenance.get('cache_line', 'Unknown')}\n"
            )

            file.write(
                f"   Cache: "
                f"{provenance.get('cache_file', 'Unknown')}\n"
            )

            if result.get(
                "matched_words"
            ):

                file.write(
                    "   Matched Terms: "
                    + ", ".join(
                        result["matched_words"]
                    )
                    + "\n"
                )

            if result.get(
                "matched_concepts"
            ):

                file.write(
                    "   Matched Concepts: "
                    + ", ".join(
                        result["matched_concepts"]
                    )
                    + "\n"
                )

        file.write(
            "=" * 70
            + "\n"
        )

    print()
    print(
        "Research saved to the Research Vault."
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

            print(
                "No saved research yet."
            )

        else:

            print(content)

    except FileNotFoundError:

        print(
            "No saved research yet."
        )

        print()

        print(
            "Research will appear here after "
            "you save your first research result."
        )

    input("\nPress Enter to continue...")


def show_trusted_sources():

    print()
    print("=" * 70)
    print("TRUSTED SOURCES")
    print("=" * 70)
    print()

    for key, source in (
        trusted_sources.items()
    ):

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
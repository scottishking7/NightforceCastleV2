from castle.research_sources import trusted_sources


def research_agent():

    while True:

        print()
        print("🔎 RESEARCH AGENT")
        print("-----------------")
        print()
        print("1 - Midnight Research")
        print("2 - Trusted Sources")
        print("3 - Saved Research")
        print("4 - Return")
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

            return

        else:

            print("❌ Invalid choice.")
            input("\nPress Enter to continue...")


def midnight_research():

    print()
    print("🌙 MIDNIGHT RESEARCH")
    print("--------------------")
    print()

    question = input("What do you want to research? ").strip()

    if not question:

        print()
        print("❌ Research question cannot be empty.")
        input("\nPress Enter to continue...")
        return

    print()
    print("Choose Research Source")
    print()

    for key, source in trusted_sources.items():

        print(f"{key} - {source['name']}")

    print("4 - Return")
    print()

    source_choice = input("Choose: ")

    if source_choice == "4":
        return

    if source_choice not in trusted_sources:

        print()
        print("❌ Invalid source.")
        input("\nPress Enter to continue...")
        return

    source = trusted_sources[source_choice]

    print()
    print("=" * 70)
    print("RESEARCH REQUEST")
    print("=" * 70)
    print()
    print("QUESTION:")
    print(question)
    print()
    print("SOURCE:")
    print(source["name"])
    print()
    print("URL:")
    print(source["url"])
    print()
    print("STATUS:")
    print("⏳ Ready for research engine")
    print()
    print("=" * 70)

    save = input("\nSave this research request? (y/n): ")

    if save.lower() == "y":

        save_research_request(
            question,
            source["name"],
            source["url"]
        )

    input("\nPress Enter to continue...")


def show_trusted_sources():

    print()
    print("🔐 TRUSTED SOURCES")
    print("------------------")
    print()

    for key, source in trusted_sources.items():

        print(f"{key} - {source['name']}")
        print(f"    {source['url']}")
        print()

    print("4 - Return")
    print()

    choice = input("Choose: ")

    if choice in trusted_sources:

        source = trusted_sources[choice]

        print()
        print(f"NAME: {source['name']}")
        print(f"URL:  {source['url']}")
        print()

        input("Press Enter to continue...")

    elif choice == "4":

        return

    else:

        print()
        print("❌ Invalid choice.")
        input("\nPress Enter to continue...")


def save_research_request(question, source_name, source_url):

    with open("vault.txt", "a", encoding="utf-8") as file:

        file.write("\n")
        file.write("========================================\n")
        file.write("RESEARCH REQUEST\n")
        file.write("========================================\n")
        file.write(f"QUESTION: {question}\n")
        file.write(f"SOURCE: {source_name}\n")
        file.write(f"URL: {source_url}\n")
        file.write("STATUS: Ready for research engine\n")
        file.write("========================================\n")

    print()
    print("✅ Research request saved to Memory Vault!")
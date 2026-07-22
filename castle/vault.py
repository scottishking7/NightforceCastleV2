def search_vault():

    print()
    print("🔎 SEARCH THE VAULT")
    print("------------------")

    search = input("Search for: ").lower()

    print()

    found = False

    with open("vault.txt", "r") as file:

        for line in file:

            if search in line.lower():

                print(f"💡 {line.strip()}")
                found = True

    if not found:
        print("❌ No matching ideas found.")

    print()


def vault_room():

    while True:

        print()
        print("📚 NIGHTFORCE MEMORY VAULT")
        print("-------------------------")
        print()
        print("1 - View Ideas")
        print("2 - Add Idea")
        print("3 - Search Ideas")
        print("4 - Return")
        print()

        choice = input("Choose: ")

        print()

        if choice == "1":

            with open("vault.txt", "r") as file:

                number = 1

                for line in file:
                    print(f"{number}. 💡 {line.strip()}")
                    number += 1

            print()

        elif choice == "2":

            idea = input("Enter your new idea: ")

            with open("vault.txt", "a+") as file:

                file.seek(0)
                content = file.read()

                if content and not content.endswith("\n"):
                    file.write("\n")

                file.write(idea + "\n")

            print()
            print("✅ Idea added!")
            print()

        elif choice == "3":

            search_vault()

        elif choice == "4":

            return

        else:

            print("❌ Unknown option.")
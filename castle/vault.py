def view_ideas():

    print()
    print("📚 IDEAS")
    print("---------")
    print()

    with open("vault.txt", "r") as file:

        ideas = file.readlines()

    if len(ideas) == 0:

        print("Vault is empty.")

    else:

        number = 1

        for idea in ideas:

            print(f"{number}. 💡 {idea.strip()}")
            number += 1

    input("\nPress Enter to continue...")


def add_idea():

    print()
    idea = input("Enter new idea: ")

    with open("vault.txt", "a") as file:

        file.write(f"\n{idea}")

    print("\n✅ Idea added!")

    input("\nPress Enter to continue...")


def search_ideas():

    print()

    search = input("Search for: ").lower()

    print()

    found = False

    with open("vault.txt", "r") as file:

        for line in file:

            if search in line.lower():

                print(f"💡 {line.strip()}")
                found = True

    if not found:

        print("❌ Nothing found.")

    input("\nPress Enter to continue...")


def delete_idea():

    with open("vault.txt", "r") as file:

        ideas = file.readlines()

    print()

    number = 1

    for idea in ideas:

        print(f"{number}. 💡 {idea.strip()}")
        number += 1

    print()

    choice = input("Delete which idea? ")

    if not choice.isdigit():

        print("❌ Invalid choice.")
        input("\nPress Enter to continue...")
        return

    choice = int(choice)

    if choice < 1 or choice > len(ideas):

        print("❌ Invalid choice.")
        input("\nPress Enter to continue...")
        return

    deleted = ideas.pop(choice - 1)

    with open("vault.txt", "w") as file:

        file.writelines(ideas)

    print()
    print(f"✅ Deleted: {deleted.strip()}")

    input("\nPress Enter to continue...")


def vault_room():

    while True:

        print()
        print("📚 NIGHTFORCE MEMORY VAULT")
        print("-------------------------")
        print("1 - View Ideas")
        print("2 - Add Idea")
        print("3 - Search Ideas")
        print("4 - Delete Idea")
        print("5 - Return to Castle")
        print("6 - Exit Castle")
        print()

        choice = input("Choose: ")

        if choice == "1":

            view_ideas()

        elif choice == "2":

            add_idea()

        elif choice == "3":

            search_ideas()

        elif choice == "4":

            delete_idea()

        elif choice == "5":

            return True

        elif choice == "6":

            return False

        else:

            print("\n❌ Unknown option.")
            input("\nPress Enter to continue...")
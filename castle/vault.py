def vault_room():

    print()
    print("📚 NIGHTFORCE MEMORY VAULT")
    print("-------------------------")
    print()

    with open("vault.txt", "r") as file:

        number = 1

        for line in file:
            print(f"{number}. 💡 {line.strip()}")
            number += 1

    print()

    answer = input("Add a new idea? (y/n): ")

    if answer.lower() == "y":

        idea = input("Enter your new idea: ")

        with open("vault.txt", "a+") as file:

            file.seek(0)
            content = file.read()

            if content and not content.endswith("\n"):
                file.write("\n")

            file.write(idea + "\n")

        print()
        print("✅ Idea added to the Vault!")
        print()
from castle.backup import backup_vault


def settings_room():

    while True:

        print()
        print("⚙️ SETTINGS")
        print("-----------")
        print()
        print("1 - Change Commander Name")
        print("2 - Castle Information")
        print("3 - Backup Memory Vault")
        print("4 - Return")
        print()

        choice = input("Choose: ")

        print()

        if choice == "1":

            with open("commander.txt", "r") as file:
                commander = file.read().strip()

            print(f"Current Commander: {commander}")
            print()

            new_name = input("Enter new Commander name: ").strip()

            if new_name:

                with open("commander.txt", "w") as file:
                    file.write(new_name)

                print()
                print("✅ Commander updated!")

            else:

                print("❌ Name cannot be empty.")

            input("\nPress Enter to continue...")

        elif choice == "2":

            print("🏰 Nightforce Castle")
            print("Version : 1.0")
            print()
            print("Installed Modules")
            print("-----------------")
            print("✅ Dashboard")
            print("✅ Memory Vault")
            print("✅ Image Prompt Builder")
            print("✅ Settings")
            print("✅ Backup System")

            input("\nPress Enter to continue...")

        elif choice == "3":

            backup_vault()

        elif choice == "4":

            return

        else:

            print("❌ Invalid option.")
            input("\nPress Enter to continue...")
from castle.banner import show_banner
from castle.menu import show_menu
from castle.vault import vault_room


def show_commander():

    with open("commander.txt", "r") as file:
        commander = file.read().strip()

    print()
    print(f"👑 Commander: {commander}")
    print()


running = True

while running:

    show_banner()
    show_commander()
    show_menu()

    choice = input("Select option (1-4): ")

    print()

    if choice == "1":

        print("🎭 Meme Workshop coming soon!")
        input("\nPress Enter to continue...")

    elif choice == "2":

        print("🎮 GTA Character Studio coming soon!")
        input("\nPress Enter to continue...")

    elif choice == "3":

        running = vault_room()

    elif choice == "4":

        print("👋 Goodbye Commander!")
        running = False

    else:

        print("❌ Unknown option.")
        input("\nPress Enter to continue...")
from castle.banner import show_banner
from castle.menu import show_menu
from castle.vault import vault_room

running = True

while running:

    show_banner()

    with open("commander.txt", "r") as file:
        commander = file.read().strip()

    print()
    print(f"👑 Commander: {commander}")
    print()

    show_menu()

    choice = input("Select option (1-4): ")

    print()

    if choice == "1":
        print("🎭 Meme Workshop coming soon!")

    elif choice == "2":
        print("🎮 GTA Character Studio coming soon!")

    elif choice == "3":
        vault_room()

    elif choice == "4":
        print("👋 Goodbye Commander!")
        running = False

    else:
        print("❌ Unknown command.")

    input("\nPress Enter to return to the Castle...")
    print()
from castle.banner import show_banner
from castle.dashboard import show_dashboard
from castle.menu import show_menu
from castle.vault import vault_room
from castle.image_builder import image_builder
from castle.settings import settings_room

running = True

while running:

    show_banner()
    show_dashboard()
    show_menu()

    choice = input("Select option (1-6): ")

    print()

    if choice == "1":

        print("🎭 Meme Workshop coming soon!")
        input("\nPress Enter to continue...")

    elif choice == "2":

        print("🚗 GTA Character Studio coming soon!")
        input("\nPress Enter to continue...")

    elif choice == "3":

        vault_room()

    elif choice == "4":

        image_builder()

    elif choice == "5":

        settings_room()

    elif choice == "6":

        print("👋 Goodbye Commander!")
        running = False

    else:

        print("❌ Invalid option.")
        input("\nPress Enter to continue...")
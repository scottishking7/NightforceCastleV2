from castle.banner import show_banner
from castle.dashboard import show_dashboard
from castle.menu import show_menu
from castle.vault import vault_room
from castle.image_builder import image_builder
from castle.settings import settings_room
from castle.social_studio import social_studio
from castle.research_agent import research_agent
from castle.trading_bot import trading_bot
from castle.midnight_radio import midnight_radio


running = True

while running:

    show_banner()
    show_dashboard()
    show_menu()

    choice = input("Select option (1-8): ")

    print()

    if choice == "1":

        trading_bot()

    elif choice == "2":

        vault_room()

    elif choice == "3":

        image_builder()

    elif choice == "4":

        social_studio()

    elif choice == "5":

        research_agent()

    elif choice == "6":

        midnight_radio()

    elif choice == "7":

        settings_room()

    elif choice == "8":

        print("👋 Goodbye Commander!")
        running = False

    else:

        print("Invalid option.")
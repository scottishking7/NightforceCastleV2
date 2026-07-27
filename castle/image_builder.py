from castle.image_styles import styles


def image_builder():

    print()
    print("🖼️ IMAGE PROMPT BUILDER")
    print("-----------------------")
    print()

    print("Choose a Style")
    print()

    for key in styles:
        print(f"{key} - {styles[key]['name']}")

    print("8 - Custom")
    print()

    choice = input("Choose style (1-8): ")

    if choice == "8":

        custom = input("Describe your custom style: ")

        subject = input("Subject: ")
        theme = input("Theme: ")
        aspect = input("Aspect Ratio: ")

        prompt = (
            f"A {custom} image featuring {subject}, themed around {theme}. "
            f"8K Ultra HD, highly detailed, aspect ratio {aspect}."
        )

    elif choice in styles:

        subject = input("Subject: ")
        theme = input("Theme: ")
        aspect = input("Aspect Ratio: ")

        prompt = styles[choice]["template"].format(
            subject=subject,
            theme=theme,
            aspect=aspect
        )

    else:

        print("❌ Invalid choice.")
        input("\nPress Enter to return...")
        return

    print()
    print("=" * 70)
    print("IMAGE PROMPT")
    print("=" * 70)
    print()
    print(prompt)
    print()
    print("=" * 70)

    save = input("\nSave this prompt to the Memory Vault? (y/n): ")

    if save.lower() == "y":

        with open("vault.txt", "a") as file:

            file.write("\n")
            file.write("========================================\n")
            file.write("IMAGE PROMPT\n")
            file.write(prompt + "\n")
            file.write("========================================\n")

        print()
        print("✅ Prompt saved!")

    input("\nPress Enter to return...")
from castle.image_styles import styles
from castle.image_options import aspect_ratios


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

    print()

    if choice == "8":

        custom = input("Describe your custom style: ")
        subject = input("Subject: ")
        theme = input("Theme: ")

        print()
        print("Choose Aspect Ratio")
        print()

        for key in aspect_ratios:
            print(f"{key} - {aspect_ratios[key]['name']}")

        print()

        aspect_choice = input("Choose (1-4): ")

        if aspect_choice not in aspect_ratios:
            print("❌ Invalid aspect ratio.")
            input("\nPress Enter to return...")
            return

        aspect = aspect_ratios[aspect_choice]["value"]

        prompt = (
            f"A {custom} image featuring {subject}, themed around {theme}. "
            f"8K Ultra HD, highly detailed, aspect ratio {aspect}."
        )

    elif choice in styles:

        subject = input("Subject: ")
        theme = input("Theme: ")

        print()
        print("Choose Aspect Ratio")
        print()

        for key in aspect_ratios:
            print(f"{key} - {aspect_ratios[key]['name']}")

        print()

        aspect_choice = input("Choose (1-4): ")

        if aspect_choice not in aspect_ratios:
            print("❌ Invalid aspect ratio.")
            input("\nPress Enter to return...")
            return

        aspect = aspect_ratios[aspect_choice]["value"]

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
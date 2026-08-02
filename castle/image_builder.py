from castle.image_styles import styles
from castle.image_options import aspect_ratios
from castle.prompt_builder import display_title, build_prompt

def image_builder():

    resolutions = {
        "1": "4K Ultra HD",
        "2": "8K Ultra HD"
    }

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

    elif choice in styles:

        subject = input("Subject: ")
        theme = input("Theme: ")

    else:

        print("❌ Invalid choice.")
        input("\nPress Enter to return...")
        return

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

    print()
    print("Choose Resolution")
    print()
    print("1 - 4K Ultra HD")
    print("2 - 8K Ultra HD")
    print()

    resolution_choice = input("Choose (1-2): ")

    if resolution_choice not in resolutions:
        print("❌ Invalid resolution.")
        input("\nPress Enter to return...")
        return

    resolution = resolutions[resolution_choice]

    if choice == "8":

        prompt = (
            f"A {custom} image featuring {subject}, themed around {theme}. "
            f"{resolution}, highly detailed, aspect ratio {aspect}."
        )

    else:

        prompt = styles[choice]["template"].format(
            subject=subject,
            theme=theme,
            aspect=aspect
        )

        prompt = prompt.replace("8K Ultra HD", resolution)
        prompt = prompt.replace("8K,", f"{resolution},")

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
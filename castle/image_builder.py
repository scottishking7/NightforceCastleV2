def image_builder():

    print()
    print("🖼️ IMAGE PROMPT BUILDER")
    print("-----------------------")
    print()

    print("Choose a Style")
    print()
    print("1 - Photorealistic")
    print("2 - Luxury Advertisement")
    print("3 - GTA Loading Screen")
    print("4 - Action Figure")
    print("5 - Movie Poster")
    print("6 - Toy Packaging")
    print("7 - Meme")
    print("8 - Custom")
    print()

    choice = input("Choose style (1-8): ")

    if choice == "1":
        style = "photorealistic"

    elif choice == "2":
        style = "luxury advertisement"

    elif choice == "3":
        style = "GTA loading screen"

    elif choice == "4":
        style = "premium collectible action figure"

    elif choice == "5":
        style = "cinematic movie poster"

    elif choice == "6":
        style = "premium toy packaging"

    elif choice == "7":
        style = "internet meme"

    elif choice == "8":
        style = input("Enter your custom style: ")

    else:
        print()
        print("❌ Invalid choice.")
        input("\nPress Enter to return...")
        return

    print()

    subject = input("Subject: ")
    theme = input("Theme: ")
    aspect = input("Aspect Ratio: ")

    print()
    print("=" * 70)
    print("IMAGE PROMPT")
    print("=" * 70)
    print()

    prompt = (
        f"A {style} featuring {subject}, "
        f"themed around {theme}. "
        f"Ultra-detailed, cinematic lighting, realistic textures, "
        f"8K resolution, aspect ratio {aspect}."
    )

    print(prompt)

    print()
    print("=" * 70)

    input("\nPress Enter to return...")
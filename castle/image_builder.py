def image_builder():

    print()
    print("🖼️ IMAGE PROMPT BUILDER")
    print("-----------------------")
    print()

    subject = input("Subject: ")
    style = input("Style: ")
    theme = input("Theme: ")
    aspect = input("Aspect Ratio: ")

    print()
    print("=" * 60)
    print("IMAGE PROMPT")
    print("=" * 60)
    print()

    prompt = (
        f"A {style.lower()} 8K image of {subject}, "
        f"themed around {theme}. "
        f"Cinematic lighting, highly detailed, "
        f"aspect ratio {aspect}."
    )

    print(prompt)

    print()
    print("=" * 60)

    input("\nPress Enter to return...")
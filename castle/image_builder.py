def image_builder():

    styles = {
        "1": {
            "name": "Photorealistic",
            "template": "A photorealistic 8K Ultra HD image of {subject}, themed around {theme}. Cinematic lighting, highly detailed, realistic textures, sharp focus, professional photography, aspect ratio {aspect}."
        },

        "2": {
            "name": "Luxury Advertisement",
            "template": "A luxury advertisement featuring {subject}, themed around {theme}. Premium product photography, elegant composition, dramatic lighting, luxury branding aesthetic, ultra-realistic materials, 8K Ultra HD, aspect ratio {aspect}."
        },

        "3": {
            "name": "GTA Loading Screen",
            "template": "A videogame-inspired loading screen featuring {subject}, themed around {theme}. Bold composition, vibrant colours, dramatic pose, stylised realism, premium artwork, highly detailed, 8K, aspect ratio {aspect}."
        },

        "4": {
            "name": "Action Figure",
            "template": "A premium collectible action figure of {subject}, themed around {theme}. Premium retail packaging, realistic plastic materials, sharp readable packaging text, cinematic studio lighting, toy-commercial quality, ultra-detailed sculpt, 8K Ultra HD, aspect ratio {aspect}."
        },

        "5": {
            "name": "Movie Poster",
            "template": "A cinematic movie poster featuring {subject}, themed around {theme}. Epic composition, dramatic lighting, theatrical atmosphere, premium poster design, ultra-detailed, 8K Ultra HD, aspect ratio {aspect}."
        },

        "6": {
            "name": "Toy Packaging",
            "template": "Premium toy packaging featuring {subject}, themed around {theme}. Clean retail presentation, realistic materials, readable product text, studio lighting, collectible quality, 8K Ultra HD, aspect ratio {aspect}."
        },

        "7": {
            "name": "Meme",
            "template": "A funny internet meme featuring {subject}, themed around {theme}. Clean composition, expressive reactions, space for readable captions, social-media ready, highly detailed, aspect ratio {aspect}."
        }
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
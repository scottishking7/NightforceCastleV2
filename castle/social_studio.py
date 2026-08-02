def social_studio():

    while True:

        print()
        print("✍️ SOCIAL STUDIO")
        print("----------------")
        print()
        print("1 - LinkedIn Post")
        print("2 - X Post")
        print("3 - Return")
        print()

        choice = input("Choose: ")

        print()

        if choice == "1":
            linkedin_post()

        elif choice == "2":
            x_post()

        elif choice == "3":
            return

        else:
            print("❌ Invalid choice.")
            input("\nPress Enter to continue...")


def linkedin_post():

    print()
    print("💼 LINKEDIN POST GENERATOR")
    print("--------------------------")
    print()

    topic = input("Topic: ").strip()
    audience = input("Audience: ").strip()

    print()
    print("Choose Tone")
    print()
    print("1 - Professional")
    print("2 - Educational")
    print("3 - Storytelling")
    print("4 - Thought Leadership")
    print()

    tone_choice = input("Choose (1-4): ")

    tones = {
        "1": "Professional",
        "2": "Educational",
        "3": "Storytelling",
        "4": "Thought Leadership"
    }

    tone = tones.get(tone_choice, "Professional")

    post = (
        f"{topic} is changing the way people think about the future.\n\n"
        f"For {audience}, the important question isn't simply "
        f"what the technology can do — it's how we can use it "
        f"to create something genuinely useful.\n\n"
        f"This is where {topic} becomes interesting.\n\n"
        f"The opportunity is to move beyond the hype and focus "
        f"on practical value, better experiences and real-world results.\n\n"
        f"That's the conversation we should be having."
    )

    print()
    print("=" * 70)
    print("LINKEDIN POST")
    print("=" * 70)
    print()
    print(post)
    print()
    print("KEY TAKEAWAY:")
    print(f"The biggest opportunity with {topic} is turning technology into practical value.")
    print()
    print("CALL TO ACTION:")
    print("What do you think the biggest opportunity is?")
    print()
    print("HASHTAGS:")
    print(f"#{topic.replace(' ', '')} #Web3 #Technology #Innovation")
    print()
    print("TONE:")
    print(tone)
    print()
    print("=" * 70)

    save_social_post("LinkedIn", post)

    input("\nPress Enter to continue...")


def x_post():

    print()
    print("🐦 X POST GENERATOR")
    print("------------------")
    print()

    topic = input("Topic: ").strip()

    print()
    print("Choose Style")
    print()
    print("1 - Educational")
    print("2 - Funny")
    print("3 - Web3")
    print("4 - Thought Leadership")
    print("5 - Breaking News")
    print()

    style_choice = input("Choose (1-5): ")

    styles = {
        "1": "Educational",
        "2": "Funny",
        "3": "Web3",
        "4": "Thought Leadership",
        "5": "Breaking News"
    }

    style = styles.get(style_choice, "Educational")

    print()
    print("Choose Hook")
    print()
    print("1 - Strong Statement")
    print("2 - Question")
    print("3 - Contrarian")
    print("4 - Curiosity")
    print()

    hook_choice = input("Choose (1-4): ")

    hooks = {
        "1": f"{topic} is changing the game.",
        "2": f"What if {topic} isn't what you think it is?",
        "3": f"Most people are looking at {topic} completely wrong.",
        "4": f"There's something about {topic} that people are missing."
    }

    hook = hooks.get(
        hook_choice,
        f"{topic} is changing the game."
    )

    post = (
        f"{hook}\n\n"
        f"The interesting part isn't the hype.\n\n"
        f"It's what happens when the technology moves "
        f"from speculation into real-world use.\n\n"
        f"That's where things get interesting. 👀"
    )

    print()
    print("=" * 70)
    print("X POST")
    print("=" * 70)
    print()
    print(post)
    print()
    print("STYLE:")
    print(style)
    print()
    print("HASHTAGS:")
    print(f"#{topic.replace(' ', '')} #Web3")
    print()
    print("=" * 70)

    save_social_post("X", post)

    input("\nPress Enter to continue...")


def save_social_post(platform, post):

    print()
    save = input("Save this post to the Memory Vault? (y/n): ")

    if save.lower() == "y":

        with open("vault.txt", "a", encoding="utf-8") as file:

            file.write("\n")
            file.write("========================================\n")
            file.write(f"{platform.upper()} POST\n")
            file.write("========================================\n")
            file.write(post + "\n")
            file.write("========================================\n")

        print()
        print("✅ Post saved to Memory Vault!")
def show_dashboard():

    with open("commander.txt", "r") as file:
        commander = file.read().strip()

    with open("vault.txt", "r") as file:
        lines = file.readlines()

    ideas = 0
    prompts = 0

    for line in lines:

        text = line.strip()

        if text == "":
            continue

        if text == "IMAGE PROMPT":
            prompts += 1

        elif (
            text != "========================================"
            and not text.startswith("Subject:")
            and not text.startswith("Style:")
            and not text.startswith("Theme:")
            and not text.startswith("Aspect Ratio:")
            and not text.startswith("Prompt:")
        ):
            ideas += 1

    total = ideas + prompts

    print()
    print("=" * 60)
    print("🏰 NIGHTFORCE CASTLE")
    print("=" * 60)
    print()
    print(f"👑 Commander        : {commander}")
    print()
    print(f"💡 Ideas            : {ideas}")
    print(f"🖼 Image Prompts    : {prompts}")
    print(f"📦 Total Assets     : {total}")
    print()
    print("=" * 60)
    print()
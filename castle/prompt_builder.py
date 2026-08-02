def display_title():

    print()
    print("🖼️ IMAGE PROMPT BUILDER")
    print("-----------------------")
    print()


def display_section(title):

    print()
    print(title)
    print("-" * len(title))
    print()


def pause():

    input("\nPress Enter to return...")


def build_prompt(template, subject, theme, aspect):

    return template.format(
        subject=subject,
        theme=theme,
        aspect=aspect
    )
import tkinter as tk


WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 700


def launch_castle():

    root = tk.Tk()

    root.title("Nightforce Castle")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.minsize(900, 600)

    # Nightforce Castle colours
    stone_dark = "#090B14"
    stone = "#111522"
    stone_light = "#1B2030"
    purple = "#6C4AB6"
    purple_dark = "#3D286B"
    teal = "#19D3C5"
    silver = "#B8C0D0"
    white = "#F2F2F2"

    root.configure(bg=stone_dark)

    # ============================================================
    # CASTLE HEADER
    # ============================================================

    header = tk.Frame(
        root,
        bg=stone_dark,
        height=110
    )

    header.pack(
        fill="x"
    )

    title = tk.Label(
        header,
        text="🏰 NIGHTFORCE CASTLE",
        font=("Segoe UI", 28, "bold"),
        bg=stone_dark,
        fg=white
    )

    title.pack(
        pady=(25, 2)
    )

    subtitle = tk.Label(
        header,
        text="THE GREAT HALL",
        font=("Segoe UI", 11, "bold"),
        bg=stone_dark,
        fg=teal
    )

    subtitle.pack()

    # ============================================================
    # MAIN CASTLE HALL
    # ============================================================

    hall = tk.Frame(
        root,
        bg=stone,
        highlightbackground=purple_dark,
        highlightthickness=3
    )

    hall.pack(
        padx=45,
        pady=20,
        fill="both",
        expand=True
    )

    # ============================================================
    # THRONE / COMMAND AREA
    # ============================================================

    command_frame = tk.Frame(
        hall,
        bg=stone_light,
        highlightbackground=purple,
        highlightthickness=2
    )

    command_frame.pack(
        padx=35,
        pady=(30, 20),
        fill="x"
    )

    command_title = tk.Label(
        command_frame,
        text="⚔  CASTLE COMMAND",
        font=("Segoe UI", 18, "bold"),
        bg=stone_light,
        fg=white
    )

    command_title.pack(
        pady=(18, 4)
    )

    command_text = tk.Label(
        command_frame,
        text="The heart of Nightforce Castle",
        font=("Segoe UI", 11),
        bg=stone_light,
        fg=teal
    )

    command_text.pack(
        pady=(0, 18)
    )

    # ============================================================
    # CASTLE ROOMS
    # ============================================================

    rooms = tk.Frame(
        hall,
        bg=stone
    )

    rooms.pack(
        padx=35,
        pady=5,
        fill="both",
        expand=True
    )

    room_data = [
        ("📈", "MT5 TRADING BOT"),
        ("📚", "MEMORY VAULT"),
        ("🖼️", "IMAGE WORKSHOP"),
        ("✨", "SOCIAL STUDIO"),
        ("🔎", "RESEARCH AGENT"),
        ("📻", "MIDNIGHT RADIO"),
        ("⚙️", "SETTINGS"),
        ("🚪", "EXIT CASTLE")
    ]

    for index, (icon, name) in enumerate(room_data):

        row = index // 4
        column = index % 4

        room = tk.Frame(
            rooms,
            bg=stone_light,
            highlightbackground=purple_dark,
            highlightthickness=1
        )

        room.grid(
            row=row,
            column=column,
            padx=8,
            pady=8,
            sticky="nsew"
        )

        icon_label = tk.Label(
            room,
            text=icon,
            font=("Segoe UI Emoji", 24),
            bg=stone_light,
            fg=white
        )

        icon_label.pack(
            pady=(14, 4)
        )

        name_label = tk.Label(
            room,
            text=name,
            font=("Segoe UI", 9, "bold"),
            bg=stone_light,
            fg=silver
        )

        name_label.pack(
            pady=(0, 14)
        )

    for column in range(4):

        rooms.columnconfigure(
            column,
            weight=1
        )

    for row in range(2):

        rooms.rowconfigure(
            row,
            weight=1
        )

    # ============================================================
    # FOOTER
    # ============================================================

    footer = tk.Label(
        hall,
        text="NIGHTFORCE CASTLE  •  PRIVATE COMMAND CENTRE",
        font=("Segoe UI", 9),
        bg=stone,
        fg=purple
    )

    footer.pack(
        pady=(5, 18)
    )

    root.mainloop()


if __name__ == "__main__":

    launch_castle()
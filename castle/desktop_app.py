import tkinter as tk
import webbrowser
from tkinter import messagebox
import MetaTrader5 as mt5

from castle.signal_engine import calculate_signal


WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 700

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"
DEFAULT_SYMBOL = "EURUSD"

DEFAULT_RISK_PERCENT = 1.0
DEFAULT_MAX_LOT = 0.10
DEFAULT_STOP_LOSS_POINTS = 200

VAULT_PATH = "vault.txt"


# ============================================================
# COLOUR PALETTE
# ============================================================

STONE_DARK = "#08090D"
STONE = "#17181D"
STONE_LIGHT = "#24262C"

WOOD_DARK = "#2A1B14"
WOOD = "#4A3023"
WOOD_LIGHT = "#6A4732"

BRONZE = "#9A7138"

PURPLE = "#6C4AB6"
PURPLE_DARK = "#3D286B"

TEAL = "#19D3C5"
SILVER = "#B8C0D0"
WHITE = "#F2F2F2"


# ============================================================
# CASTLE STONE MASONRY
# ============================================================

def add_stone_masonry(parent):

    canvas = tk.Canvas(
        parent,
        bg=STONE,
        highlightthickness=0,
        bd=0
    )

    canvas.place(
        x=0,
        y=0,
        relwidth=1,
        relheight=1
    )

    def draw_stones(event=None):

        canvas.delete("stone")

        width = max(canvas.winfo_width(), 700)
        height = max(canvas.winfo_height(), 400)

        stone_width = 125
        stone_height = 70

        stone_colours = [
            "#202329",
            "#25282E",
            "#292C32",
            "#1D2026",
            "#30333A",
            "#22252B"
        ]

        row = 0
        y = -stone_height

        while y < height + stone_height:

            offset = 0

            if row % 2:
                offset = stone_width // 2

            column = 0
            x = -stone_width + offset

            while x < width + stone_width:

                colour_index = (row * 5 + column * 3) % len(stone_colours)
                fill_colour = stone_colours[colour_index]

                variation = (row + column) % 4

                left = x + 3
                top = y + 3
                right = x + stone_width - 4
                bottom = y + stone_height - 4

                if variation == 0:

                    points = [
                        left + 8, top,
                        right - 10, top + 2,
                        right, top + 16,
                        right - 5, bottom - 9,
                        right - 25, bottom,
                        left + 5, bottom - 5,
                        left, top + 18
                    ]

                elif variation == 1:

                    points = [
                        left + 2, top + 8,
                        left + 20, top,
                        right - 5, top + 5,
                        right, top + 25,
                        right - 12, bottom,
                        left + 10, bottom - 3,
                        left, top + 35
                    ]

                elif variation == 2:

                    points = [
                        left + 12, top,
                        right - 4, top + 4,
                        right, top + 30,
                        right - 15, bottom - 2,
                        left + 18, bottom,
                        left, bottom - 14,
                        left + 3, top + 18
                    ]

                else:

                    points = [
                        left + 5, top + 4,
                        right - 18, top,
                        right, top + 12,
                        right - 4, bottom - 5,
                        right - 25, bottom,
                        left + 2, bottom - 10,
                        left, top + 25
                    ]

                canvas.create_polygon(
                    points,
                    fill=fill_colour,
                    outline="#101217",
                    width=4,
                    tags="stone"
                )

                highlight_points = [
                    points[0],
                    points[1],
                    points[2],
                    points[3],
                    points[4],
                    points[5]
                ]

                canvas.create_line(
                    highlight_points,
                    fill="#3A3E46",
                    width=2,
                    tags="stone"
                )

                column += 1
                x += stone_width

            row += 1
            y += stone_height

        def draw_wall_torch(x, y):

            # Soft firelight rings behind the flame.
            canvas.create_oval(
                x - 34, y - 38,
                x + 34, y + 32,
                fill="#4A2B18",
                outline="",
                tags="stone"
            )

            canvas.create_oval(
                x - 23, y - 30,
                x + 23, y + 20,
                fill="#70401F",
                outline="",
                tags="stone"
            )

            # Black iron wall bracket.
            canvas.create_line(
                x, y + 18,
                x, y + 34,
                fill="#090A0D",
                width=6,
                tags="stone"
            )

            canvas.create_line(
                x - 11, y + 34,
                x + 11, y + 34,
                fill="#090A0D",
                width=5,
                tags="stone"
            )

            canvas.create_line(
                x, y + 29,
                x + 13, y + 21,
                fill="#17181D",
                width=4,
                tags="stone"
            )

            # Wooden torch shaft.
            canvas.create_polygon(
                x - 5, y + 8,
                x + 5, y + 8,
                x + 3, y + 32,
                x - 3, y + 32,
                fill=WOOD,
                outline=WOOD_DARK,
                width=2,
                tags="stone"
            )

            # Dark wrapping beneath the flame.
            canvas.create_rectangle(
                x - 8, y + 3,
                x + 8, y + 15,
                fill="#17120F",
                outline="#090A0D",
                width=2,
                tags="stone"
            )

            # Outer flame.
            canvas.create_polygon(
                x, y - 32,
                x + 11, y - 13,
                x + 8, y + 2,
                x, y + 9,
                x - 10, y + 1,
                x - 12, y - 12,
                x - 5, y - 22,
                fill="#D96A1D",
                outline="#7A3213",
                width=1,
                tags="stone"
            )

            # Inner flame.
            canvas.create_polygon(
                x, y - 21,
                x + 6, y - 8,
                x + 4, y + 1,
                x, y + 5,
                x - 5, y,
                x - 5, y - 8,
                fill="#F2B544",
                outline="",
                tags="stone"
            )

            # Hot flame core.
            canvas.create_oval(
                x - 3, y - 8,
                x + 3, y + 2,
                fill="#FFE29A",
                outline="",
                tags="stone"
            )

        # Torches mounted on the exposed outer Great Hall walls.
        torch_y = 65
        draw_wall_torch(42, torch_y)
        draw_wall_torch(width - 42, torch_y)

    canvas.bind("<Configure>", draw_stones)

    return canvas


def launch_castle():

    root = tk.Tk()

    root.title("Nightforce Castle")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.minsize(900, 600)

    root.configure(bg=STONE_DARK)

    show_great_hall(root)

    root.mainloop()


# ============================================================
# GREAT HALL
# ============================================================

def show_great_hall(root):

    clear_window(root)

    header = tk.Frame(
        root,
        bg=STONE_DARK
    )

    header.pack(fill="x")

    title = tk.Label(
        header,
        text="\U0001F3F0 NIGHTFORCE CASTLE",
        font=("Perpetua Titling MT", 28, "bold"),
        bg=STONE_DARK,
        fg=WHITE
    )

    title.pack(pady=(25, 2))

    subtitle = tk.Label(
        header,
        text="THE GREAT HALL",
        font=("Copperplate Gothic Light", 11, "bold"),
        bg=STONE_DARK,
        fg=TEAL
    )

    subtitle.pack()

    title_divider = tk.Frame(
        header,
        bg=BRONZE,
        height=2
    )

    title_divider.pack(
        fill="x",
        padx=170,
        pady=(8, 4)
    )

    hall = tk.Frame(
        root,
        bg=STONE,
        highlightbackground=WOOD,
        highlightthickness=6,
        relief="ridge",
        bd=2
    )

    hall.pack(
        padx=45,
        pady=20,
        fill="both",
        expand=True
    )

    add_stone_masonry(hall)

    timber_top = tk.Frame(
        hall,
        bg=WOOD,
        height=18,
        highlightbackground=WOOD_DARK,
        highlightcolor=WOOD_DARK,
        highlightthickness=3,
        relief="raised",
        bd=2
    )

    timber_top.pack(
        fill="x",
        padx=18,
        pady=(18, 0)
    )

    timber_top_highlight = tk.Frame(
        timber_top,
        bg=WOOD_LIGHT,
        height=3
    )
    timber_top_highlight.pack(fill="x", padx=4, pady=(2, 0))

    timber_bottom = tk.Frame(
        hall,
        bg=WOOD,
        height=18,
        highlightbackground=WOOD_DARK,
        highlightcolor=WOOD_DARK,
        highlightthickness=3,
        relief="raised",
        bd=2
    )

    timber_bottom.pack(
        fill="x",
        padx=18,
        pady=(0, 18)
    )

    timber_bottom_highlight = tk.Frame(
        timber_bottom,
        bg=WOOD_LIGHT,
        height=3
    )
    timber_bottom_highlight.pack(fill="x", padx=4, pady=(2, 0))

    command_frame = tk.Frame(
        hall,
        bg=STONE_LIGHT,
        highlightbackground=BRONZE,
        highlightthickness=3,
        relief="ridge",
        bd=2
    )

    command_frame.pack(
        padx=35,
        pady=(14, 10),
        fill="x"
    )

    command_title = tk.Label(
        command_frame,
        text="\u2694  CASTLE COMMAND",
        font=("Perpetua Titling MT", 18, "bold"),
        bg=STONE_LIGHT,
        fg=WHITE
    )

    command_title.pack(pady=(18, 4))

    command_text = tk.Label(
        command_frame,
        text="The heart of Nightforce Castle",
        font=("Goudy Old Style", 12),
        bg=STONE_LIGHT,
        fg=TEAL
    )

    command_row = tk.Frame(
        command_frame,
        bg=STONE_LIGHT
    )

    command_row.pack(
        pady=(0, 14)
    )

    command_text.pack(
        in_=command_row,
        side="left",
        padx=(0, 18)
    )

    midnight_hq_button = tk.Button(
        command_row,
        text="\U0001F319  ENTER MIDNIGHT HQ",
        command=lambda: open_midnight_hq(root),
        font=("Goudy Old Style", 11, "bold"),
        bg=PURPLE_DARK,
        fg=TEAL,
        activebackground=TEAL,
        activeforeground=STONE_DARK,
        highlightbackground=BRONZE,
        highlightthickness=2,
        relief="raised",
        bd=2,
        cursor="hand2",
        padx=18,
        pady=4
    )

    midnight_hq_button.pack(
        side="left"
    )

    rooms = tk.Frame(
        hall,
        bg=STONE
    )

    rooms.pack(
        padx=35,
        pady=5,
        fill="both",
        expand=True
    )

    room_data = [
        ("\U0001F4C8", "MT5 TRADING BOT", open_mt5_room),
        ("\U0001F4DA", "MEMORY VAULT", open_memory_vault),
        ("\U0001F5BC", "IMAGE WORKSHOP", None),
        ("\u2728", "SOCIAL STUDIO", None),
        ("\U0001F50E", "RESEARCH AGENT", None),
        ("\U0001F4FB", "MIDNIGHT RADIO", None),
        ("\u2699", "SETTINGS", None),
        ("\U0001F6AA", "EXIT CASTLE", root.destroy)
    ]

    for index, (icon, name, command) in enumerate(room_data):

        row = index // 4
        column = index % 4

        room = tk.Frame(
            rooms,
            bg=STONE_LIGHT,
            highlightbackground=BRONZE,
            highlightthickness=3,
            relief="ridge",
            bd=1
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
            bg=STONE_LIGHT,
            fg=WHITE
        )

        icon_label.pack(pady=(14, 4))

        bronze_accent = tk.Frame(
            room,
            bg=BRONZE,
            height=2
        )

        bronze_accent.pack(
            fill="x",
            padx=38,
            pady=(0, 5)
        )

        if command is not None:

            button = tk.Button(
                room,
                text=name,
                command=command,
                font=("Goudy Old Style", 11, "bold"),
                bg=STONE_LIGHT,
                fg=SILVER,
                activebackground=PURPLE,
                activeforeground=WHITE,
                relief="flat",
                borderwidth=0,
                cursor="hand2"
            )

            button.pack(pady=(0, 14))

        else:

            name_label = tk.Label(
                room,
                text=name,
                font=("Goudy Old Style", 11, "bold"),
                bg=STONE_LIGHT,
                fg=SILVER
            )

            name_label.pack(pady=(0, 14))

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

    footer = tk.Label(
        hall,
        text="NIGHTFORCE CASTLE  \u2022  PRIVATE COMMAND CENTRE",
        font=("Segoe UI", 9),
        bg=STONE,
        fg=PURPLE
    )

    footer.pack(pady=(5, 18))


# ============================================================
# OFFICIAL MIDNIGHT
# ============================================================

def open_official_midnight(root=None):

    if root is None:
        root = tk._default_root

    clear_window(root)

    header = tk.Frame(
        root,
        bg=STONE_DARK
    )
    header.pack(fill="x")

    title = tk.Label(
        header,
        text="\U0001F319 OFFICIAL MIDNIGHT",
        font=("Perpetua Titling MT", 28, "bold"),
        bg=STONE_DARK,
        fg=WHITE
    )
    title.pack(pady=(25, 2))

    subtitle = tk.Label(
        header,
        text="VERIFIED MIDNIGHT NETWORK RESOURCES",
        font=("Copperplate Gothic Light", 11, "bold"),
        bg=STONE_DARK,
        fg=TEAL
    )
    subtitle.pack()

    title_divider = tk.Frame(
        header,
        bg=BRONZE,
        height=2
    )
    title_divider.pack(
        fill="x",
        padx=170,
        pady=(8, 4)
    )

    panel = tk.Frame(
        root,
        bg=STONE,
        highlightbackground=BRONZE,
        highlightthickness=3
    )
    panel.pack(
        padx=45,
        pady=20,
        fill="both",
        expand=True
    )

    intro = tk.Label(
        panel,
        text="Official Midnight Network destinations will be available from this command desk.",
        font=("Goudy Old Style", 13),
        bg=STONE,
        fg=SILVER
    )
    intro.pack(pady=(35, 20))

    status = tk.Label(
        panel,
        text="OFFICIAL RESOURCE DESK ONLINE",
        font=("Goudy Old Style", 12, "bold"),
        bg=STONE_LIGHT,
        fg=TEAL,
        padx=30,
        pady=20
    )
    status.pack(
        padx=80,
        pady=20,
        fill="x"
    )

    official_site_button = tk.Button(
        panel,
        text="\U0001F310  OFFICIAL MIDNIGHT WEBSITE",
        command=lambda: webbrowser.open("https://midnight.network/"),
        font=("Goudy Old Style", 11, "bold"),
        bg=PURPLE_DARK,
        fg=TEAL,
        activebackground=TEAL,
        activeforeground=STONE_DARK,
        highlightbackground=BRONZE,
        highlightthickness=2,
        relief="raised",
        bd=2,
        cursor="hand2",
        padx=25,
        pady=10
    )
    official_site_button.pack(
        padx=80,
        pady=(5, 10),
        fill="x"
    )

    developer_docs_button = tk.Button(
        panel,
        text="\U0001F4D6  OFFICIAL DEVELOPER DOCS",
        command=lambda: webbrowser.open("https://docs.midnight.network/"),
        font=("Goudy Old Style", 11, "bold"),
        bg=PURPLE_DARK,
        fg=TEAL,
        activebackground=TEAL,
        activeforeground=STONE_DARK,
        highlightbackground=BRONZE,
        highlightthickness=2,
        relief="raised",
        bd=2,
        cursor="hand2",
        padx=25,
        pady=10
    )
    developer_docs_button.pack(
        padx=80,
        pady=(0, 10),
        fill="x"
    )

    ecosystem_button = tk.Button(
        panel,
        text="\U0001F310  MIDNIGHT ECOSYSTEM CATALOG",
        command=lambda: webbrowser.open("https://midnight.network/ecosystem-catalog"),
        font=("Goudy Old Style", 11, "bold"),
        bg=PURPLE_DARK,
        fg=TEAL,
        activebackground=TEAL,
        activeforeground=STONE_DARK,
        highlightbackground=BRONZE,
        highlightthickness=2,
        relief="raised",
        bd=2,
        cursor="hand2",
        padx=25,
        pady=10
    )
    ecosystem_button.pack(
        padx=80,
        pady=(0, 10),
        fill="x"
    )

    back_button = tk.Button(
        panel,
        text="\u2190 BACK TO MIDNIGHT HQ",
        command=lambda: open_midnight_hq(root),
        font=("Goudy Old Style", 11, "bold"),
        bg=PURPLE,
        fg=WHITE,
        activebackground=TEAL,
        activeforeground=STONE_DARK,
        relief="flat",
        cursor="hand2",
        padx=20,
        pady=10
    )
    back_button.pack(pady=25)


# ============================================================
# DISCORD COMMANDS
# ============================================================

def open_discord_commands(root=None):

    if root is None:
        root = tk._default_root

    clear_window(root)

    header = tk.Frame(
        root,
        bg=STONE_DARK
    )
    header.pack(fill="x")

    title = tk.Label(
        header,
        text="\U0001F4AC DISCORD COMMANDS",
        font=("Perpetua Titling MT", 28, "bold"),
        bg=STONE_DARK,
        fg=WHITE
    )
    title.pack(pady=(25, 2))

    subtitle = tk.Label(
        header,
        text="MIDNIGHT COMMUNITY COMMAND LIBRARY",
        font=("Copperplate Gothic Light", 11, "bold"),
        bg=STONE_DARK,
        fg=TEAL
    )
    subtitle.pack()

    title_divider = tk.Frame(
        header,
        bg=BRONZE,
        height=2
    )
    title_divider.pack(
        fill="x",
        padx=170,
        pady=(8, 4)
    )

    panel = tk.Frame(
        root,
        bg=STONE,
        highlightbackground=BRONZE,
        highlightthickness=3
    )
    panel.pack(
        padx=45,
        pady=20,
        fill="both",
        expand=True
    )

    intro = tk.Label(
        panel,
        text="Search, inspect and copy useful Midnight community commands.",
        font=("Goudy Old Style", 13),
        bg=STONE,
        fg=SILVER
    )
    intro.pack(pady=(35, 20))

    search_frame = tk.Frame(
        panel,
        bg=STONE_LIGHT,
        highlightbackground=BRONZE,
        highlightthickness=2
    )
    search_frame.pack(
        padx=80,
        pady=(10, 20),
        fill="x"
    )

    search_label = tk.Label(
        search_frame,
        text="SEARCH COMMANDS",
        font=("Goudy Old Style", 11, "bold"),
        bg=STONE_LIGHT,
        fg=TEAL
    )
    search_label.pack(
        anchor="w",
        padx=18,
        pady=(14, 5)
    )

    search_entry = tk.Entry(
        search_frame,
        font=("Consolas", 12),
        bg=STONE_DARK,
        fg=WHITE,
        insertbackground=TEAL,
        relief="flat",
        bd=0
    )
    search_entry.pack(
        padx=18,
        pady=(0, 14),
        fill="x",
        ipady=8
    )

    results_frame = tk.Frame(
        panel,
        bg=STONE_LIGHT,
        highlightbackground=BRONZE,
        highlightthickness=2
    )
    results_frame.pack(
        padx=80,
        pady=(0, 15),
        fill="both",
        expand=True
    )

    results_title = tk.Label(
        results_frame,
        text="COMMAND RESULTS",
        font=("Goudy Old Style", 11, "bold"),
        bg=STONE_LIGHT,
        fg=TEAL
    )
    results_title.pack(
        anchor="w",
        padx=18,
        pady=(14, 5)
    )

    results_status = tk.Label(
        results_frame,
        text="Command library ready. Verified commands will appear here.",
        font=("Goudy Old Style", 11),
        bg=STONE_DARK,
        fg=SILVER,
        anchor="w",
        padx=15,
        pady=15
    )
    results_status.pack(
        padx=18,
        pady=(0, 10),
        fill="x"
    )

    command_rows = tk.Frame(
        results_frame,
        bg=STONE_LIGHT
    )
    command_rows.pack(
        padx=18,
        pady=(0, 14),
        fill="both",
        expand=True
    )

    command_library = []

    def copy_command(command):
        root.clipboard_clear()
        root.clipboard_append(command)
        root.update()

        results_status.configure(
            text=f"Copied to clipboard: {command}",
            fg=TEAL
        )

    def render_command_rows(commands):
        for widget in command_rows.winfo_children():
            widget.destroy()

        for item in commands:
            row = tk.Frame(
                command_rows,
                bg=STONE_DARK,
                highlightbackground=BRONZE,
                highlightthickness=1
            )
            row.pack(
                fill="x",
                pady=(0, 8)
            )

            command_label = tk.Label(
                row,
                text=item["command"],
                font=("Consolas", 11, "bold"),
                bg=STONE_DARK,
                fg=TEAL,
                anchor="w"
            )
            command_label.pack(
                side="left",
                padx=(12, 15),
                pady=12
            )

            description_label = tk.Label(
                row,
                text=item["description"],
                font=("Goudy Old Style", 11),
                bg=STONE_DARK,
                fg=WHITE,
                anchor="w"
            )
            description_label.pack(
                side="left",
                fill="x",
                expand=True,
                pady=12
            )

            copy_button = tk.Button(
                row,
                text="COPY",
                command=lambda command=item["command"]: copy_command(command),
                font=("Goudy Old Style", 10, "bold"),
                bg=PURPLE,
                fg=WHITE,
                activebackground=TEAL,
                activeforeground=STONE_DARK,
                relief="flat",
                cursor="hand2",
                padx=12,
                pady=5
            )
            copy_button.pack(
                side="right",
                padx=12,
                pady=8
            )

    def search_commands(event=None):
        query = search_entry.get().strip().lower()

        if not command_library:
            render_command_rows([])
            results_status.configure(
                text="No verified commands have been loaded yet.",
                fg=SILVER
            )
            return

        matches = [
            item
            for item in command_library
            if query in item["command"].lower()
            or query in item["description"].lower()
        ]

        if matches:
            render_command_rows(matches)
            results_status.configure(
                text=f"{len(matches)} command(s) found.",
                fg=TEAL
            )
        else:
            render_command_rows([])
            results_status.configure(
                text="No commands matched your search.",
                fg=SILVER
            )

    search_entry.bind("<KeyRelease>", search_commands)

    back_button = tk.Button(
        panel,
        text="\u2190 BACK TO MIDNIGHT HQ",
        command=lambda: open_midnight_hq(root),
        font=("Goudy Old Style", 11, "bold"),
        bg=PURPLE,
        fg=WHITE,
        activebackground=TEAL,
        activeforeground=STONE_DARK,
        relief="flat",
        cursor="hand2",
        padx=20,
        pady=10
    )
    back_button.pack(pady=25)


# ============================================================
# WALLETS & DAPPS
# ============================================================

def open_wallets_dapps(root=None):

    if root is None:
        root = tk._default_root

    clear_window(root)

    header = tk.Frame(
        root,
        bg=STONE_DARK
    )
    header.pack(fill="x")

    title = tk.Label(
        header,
        text="\U0001F45B WALLETS & DAPPS",
        font=("Perpetua Titling MT", 28, "bold"),
        bg=STONE_DARK,
        fg=WHITE
    )
    title.pack(pady=(25, 2))

    subtitle = tk.Label(
        header,
        text="MIDNIGHT WALLET & ECOSYSTEM DESK",
        font=("Copperplate Gothic Light", 11, "bold"),
        bg=STONE_DARK,
        fg=TEAL
    )
    subtitle.pack()

    title_divider = tk.Frame(
        header,
        bg=BRONZE,
        height=2
    )
    title_divider.pack(
        fill="x",
        padx=170,
        pady=(8, 4)
    )

    panel = tk.Frame(
        root,
        bg=STONE,
        highlightbackground=BRONZE,
        highlightthickness=3
    )
    panel.pack(
        padx=45,
        pady=20,
        fill="both",
        expand=True
    )

    intro = tk.Label(
        panel,
        text="Verified Midnight wallet and dApp resources will be organised here.",
        font=("Goudy Old Style", 13),
        bg=STONE,
        fg=SILVER
    )
    intro.pack(pady=(35, 20))

    status_frame = tk.Frame(
        panel,
        bg=STONE_LIGHT,
        highlightbackground=BRONZE,
        highlightthickness=2
    )
    status_frame.pack(
        padx=80,
        pady=20,
        fill="both",
        expand=True
    )

    status_label = tk.Label(
        status_frame,
        text="WALLETS & DAPPS DESK ONLINE\n\nVerified resources will be added here.",
        font=("Goudy Old Style", 12, "bold"),
        bg=STONE_LIGHT,
        fg=TEAL,
        justify="center",
        padx=20,
        pady=30
    )
    status_label.pack(expand=True)

    back_button = tk.Button(
        panel,
        text="\u2190 BACK TO MIDNIGHT HQ",
        command=lambda: open_midnight_hq(root),
        font=("Goudy Old Style", 11, "bold"),
        bg=PURPLE,
        fg=WHITE,
        activebackground=TEAL,
        activeforeground=STONE_DARK,
        relief="flat",
        cursor="hand2",
        padx=20,
        pady=10
    )
    back_button.pack(pady=25)


# ============================================================
# MIDNIGHT HQ
# ============================================================

def open_midnight_hq(root=None):

    if root is None:
        root = tk._default_root

    clear_window(root)

    header = tk.Frame(
        root,
        bg=STONE_DARK
    )
    header.pack(fill="x")

    title = tk.Label(
        header,
        text="\U0001F319 MIDNIGHT HQ",
        font=("Perpetua Titling MT", 28, "bold"),
        bg=STONE_DARK,
        fg=WHITE
    )
    title.pack(pady=(25, 2))

    subtitle = tk.Label(
        header,
        text="NIGHTFORCE MIDNIGHT COMMAND CENTRE",
        font=("Copperplate Gothic Light", 11, "bold"),
        bg=STONE_DARK,
        fg=TEAL
    )
    subtitle.pack()

    title_divider = tk.Frame(
        header,
        bg=BRONZE,
        height=2
    )
    title_divider.pack(
        fill="x",
        padx=170,
        pady=(8, 4)
    )

    panel = tk.Frame(
        root,
        bg=STONE,
        highlightbackground=BRONZE,
        highlightthickness=3
    )
    panel.pack(
        padx=45,
        pady=20,
        fill="both",
        expand=True
    )

    intro = tk.Label(
        panel,
        text="Midnight resources, Nightforce tools and community intelligence",
        font=("Goudy Old Style", 13),
        bg=STONE,
        fg=SILVER
    )
    intro.pack(pady=(25, 15))

    status_frame = tk.Frame(
        panel,
        bg=STONE_LIGHT,
        highlightbackground=PURPLE_DARK,
        highlightthickness=2
    )
    status_frame.pack(
        padx=80,
        pady=20,
        fill="x"
    )

    status_label = tk.Label(
        status_frame,
        text="MIDNIGHT HQ ONLINE\n\nResource systems will be added here.",
        font=("Goudy Old Style", 12, "bold"),
        bg=STONE_LIGHT,
        fg=TEAL,
        justify="center",
        padx=20,
        pady=25
    )
    status_label.pack()

    resource_grid = tk.Frame(
        panel,
        bg=STONE
    )
    resource_grid.pack(
        padx=45,
        pady=(0, 10),
        fill="both",
        expand=True
    )

    resource_data = [
        ("\U0001F319", "OFFICIAL MIDNIGHT"),
        ("\U0001F4AC", "DISCORD COMMANDS"),
        ("\U0001F45B", "WALLETS & DAPPS"),
        ("\U0001F6E0", "DEVELOPER DESK"),
        ("\U0001F6E1", "SECURITY DESK"),
        ("\u2694", "NIGHTFORCE")
    ]

    for index, (icon, name) in enumerate(resource_data):

        row = index // 3
        column = index % 3

        resource = tk.Frame(
            resource_grid,
            bg=STONE_LIGHT,
            highlightbackground=BRONZE,
            highlightthickness=2,
            relief="ridge",
            bd=1
        )
        resource.grid(
            row=row,
            column=column,
            padx=7,
            pady=7,
            sticky="nsew"
        )

        resource_icon = tk.Label(
            resource,
            text=icon,
            font=("Segoe UI Emoji", 20),
            bg=STONE_LIGHT,
            fg=WHITE
        )
        resource_icon.pack(pady=(9, 2))

        resource_name = tk.Label(
            resource,
            text=name,
            font=("Goudy Old Style", 10, "bold"),
            bg=STONE_LIGHT,
            fg=TEAL
        )
        resource_name.pack(pady=(0, 9))

        if name == "OFFICIAL MIDNIGHT":
            resource.configure(cursor="hand2")
            resource_icon.configure(cursor="hand2")
            resource_name.configure(cursor="hand2")

            resource.bind(
                "<Button-1>",
                lambda event: open_official_midnight(root)
            )
            resource_icon.bind(
                "<Button-1>",
                lambda event: open_official_midnight(root)
            )
            resource_name.bind(
                "<Button-1>",
                lambda event: open_official_midnight(root)
            )

        if name == "DISCORD COMMANDS":
            resource.configure(cursor="hand2")
            resource_icon.configure(cursor="hand2")
            resource_name.configure(cursor="hand2")

            resource.bind(
                "<Button-1>",
                lambda event: open_discord_commands(root)
            )
            resource_icon.bind(
                "<Button-1>",
                lambda event: open_discord_commands(root)
            )
            resource_name.bind(
                "<Button-1>",
                lambda event: open_discord_commands(root)
            )

        if name == "WALLETS & DAPPS":
            resource.configure(cursor="hand2")
            resource_icon.configure(cursor="hand2")
            resource_name.configure(cursor="hand2")

            resource.bind(
                "<Button-1>",
                lambda event: open_wallets_dapps(root)
            )
            resource_icon.bind(
                "<Button-1>",
                lambda event: open_wallets_dapps(root)
            )
            resource_name.bind(
                "<Button-1>",
                lambda event: open_wallets_dapps(root)
            )

    for column in range(3):
        resource_grid.columnconfigure(column, weight=1)

    for row in range(2):
        resource_grid.rowconfigure(row, weight=1)

    back_button = tk.Button(
        panel,
        text="\u2190 BACK TO GREAT HALL",
        command=lambda: show_great_hall(root),
        font=("Goudy Old Style", 11, "bold"),
        bg=PURPLE,
        fg=WHITE,
        activebackground=TEAL,
        activeforeground=STONE_DARK,
        relief="flat",
        cursor="hand2",
        padx=20,
        pady=10
    )
    back_button.pack(pady=25)


# ============================================================
# MEMORY VAULT
# ============================================================

def open_memory_vault(root=None):

    if root is None:

        root = tk._default_root

    clear_window(root)

    header = tk.Frame(
        root,
        bg=STONE_DARK
    )

    header.pack(fill="x")

    title = tk.Label(
        header,
        text="ðŸ“š MEMORY VAULT",
        font=("Segoe UI", 28, "bold"),
        bg=STONE_DARK,
        fg=WHITE
    )

    title.pack(pady=(25, 2))

    subtitle = tk.Label(
        header,
        text="NIGHTFORCE KNOWLEDGE ARCHIVE",
        font=("Segoe UI", 11, "bold"),
        bg=STONE_DARK,
        fg=TEAL
    )

    subtitle.pack()

    panel = tk.Frame(
        root,
        bg=STONE,
        highlightbackground=PURPLE_DARK,
        highlightthickness=3
    )

    panel.pack(
        padx=45,
        pady=20,
        fill="both",
        expand=True
    )

    intro = tk.Label(
        panel,
        text="Your saved ideas, prompts, posts and research requests",
        font=("Segoe UI", 11),
        bg=STONE,
        fg=SILVER
    )

    intro.pack(pady=(15, 10))

    button_frame = tk.Frame(
        panel,
        bg=STONE
    )

    button_frame.pack(
        fill="x",
        padx=30,
        pady=5
    )

    view_button = tk.Button(
        button_frame,
        text="ðŸ“– VIEW VAULT",
        command=lambda: show_vault_contents(root),
        font=("Segoe UI", 11, "bold"),
        bg=PURPLE,
        fg=WHITE,
        activebackground=TEAL,
        activeforeground=STONE_DARK,
        relief="flat",
        padx=20,
        pady=10
    )

    view_button.pack(
        side="left",
        padx=8
    )

    add_button = tk.Button(
        button_frame,
        text="âž• ADD MEMORY",
        command=lambda: add_memory(root),
        font=("Segoe UI", 11, "bold"),
        bg=PURPLE,
        fg=WHITE,
        activebackground=TEAL,
        activeforeground=STONE_DARK,
        relief="flat",
        padx=20,
        pady=10
    )

    add_button.pack(
        side="left",
        padx=8
    )

    search_button = tk.Button(
        button_frame,
        text="ðŸ”Ž SEARCH VAULT",
        command=lambda: search_vault(root),
        font=("Segoe UI", 11, "bold"),
        bg=STONE_LIGHT,
        fg=TEAL,
        activebackground=PURPLE,
        activeforeground=WHITE,
        relief="flat",
        padx=20,
        pady=10
    )

    search_button.pack(
        side="left",
        padx=8
    )

    status_frame = tk.Frame(
        panel,
        bg=STONE_LIGHT,
        highlightbackground=PURPLE,
        highlightthickness=2
    )

    status_frame.pack(
        padx=100,
        pady=25,
        fill="x"
    )

    try:

        with open(VAULT_PATH, "r", encoding="utf-8") as file:

            lines = file.readlines()

        memory_count = len(
            [
                line
                for line in lines
                if line.strip()
            ]
        )

        status_text = (
            f"âœ“ VAULT CONNECTED\n\n"
            f"{memory_count} saved lines currently stored"
        )

    except FileNotFoundError:

        status_text = (
            "âš  VAULT FILE NOT FOUND\n\n"
            "The vault will be created when you add your first memory."
        )

    status_label = tk.Label(
        status_frame,
        text=status_text,
        font=("Segoe UI", 12, "bold"),
        bg=STONE_LIGHT,
        fg=TEAL,
        justify="center",
        padx=20,
        pady=20
    )

    status_label.pack()

    safety_label = tk.Label(
        panel,
        text="âœ“ EXISTING VAULT PRESERVED â€¢ NOTHING IS DELETED",
        font=("Segoe UI", 10, "bold"),
        bg=STONE,
        fg=PURPLE
    )

    safety_label.pack(pady=10)

    back_button = tk.Button(
        panel,
        text="â† RETURN TO GREAT HALL",
        command=lambda: show_great_hall(root),
        font=("Segoe UI", 11, "bold"),
        bg=STONE_DARK,
        fg=TEAL,
        activebackground=PURPLE,
        activeforeground=WHITE,
        relief="flat",
        padx=25,
        pady=10
    )

    back_button.pack(
        pady=(10, 20)
    )


# ============================================================
# VIEW VAULT CONTENTS
# ============================================================

def show_vault_contents(root):

    clear_window(root)

    header = tk.Frame(
        root,
        bg=STONE_DARK
    )

    header.pack(fill="x")

    title = tk.Label(
        header,
        text="ðŸ“– VAULT ARCHIVE",
        font=("Segoe UI", 26, "bold"),
        bg=STONE_DARK,
        fg=WHITE
    )

    title.pack(pady=(20, 2))

    subtitle = tk.Label(
        header,
        text="SAVED NIGHTFORCE MATERIAL",
        font=("Segoe UI", 10, "bold"),
        bg=STONE_DARK,
        fg=TEAL
    )

    subtitle.pack()

    panel = tk.Frame(
        root,
        bg=STONE,
        highlightbackground=PURPLE_DARK,
        highlightthickness=3
    )

    panel.pack(
        padx=45,
        pady=15,
        fill="both",
        expand=True
    )

    text_frame = tk.Frame(
        panel,
        bg=STONE
    )

    text_frame.pack(
        padx=20,
        pady=20,
        fill="both",
        expand=True
    )

    scrollbar = tk.Scrollbar(
        text_frame
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    text_box = tk.Text(
        text_frame,
        bg=STONE_LIGHT,
        fg=WHITE,
        insertbackground=WHITE,
        font=("Segoe UI", 10),
        wrap="word",
        yscrollcommand=scrollbar.set,
        relief="flat",
        padx=15,
        pady=15
    )

    text_box.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.config(
        command=text_box.yview
    )

    try:

        with open(
            VAULT_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            contents = file.read()

        if contents.strip():

            text_box.insert(
                "1.0",
                contents
            )

        else:

            text_box.insert(
                "1.0",
                "Vault is currently empty."
            )

    except FileNotFoundError:

        text_box.insert(
            "1.0",
            "Vault file does not exist yet."
        )

    text_box.config(
        state="disabled"
    )

    back_button = tk.Button(
        panel,
        text="â† RETURN TO MEMORY VAULT",
        command=lambda: open_memory_vault(root),
        font=("Segoe UI", 10, "bold"),
        bg=STONE_DARK,
        fg=TEAL,
        activebackground=PURPLE,
        activeforeground=WHITE,
        relief="flat",
        padx=25,
        pady=8
    )

    back_button.pack(
        pady=(0, 15)
    )


# ============================================================
# ADD MEMORY
# ============================================================

def add_memory(root):

    clear_window(root)

    header = tk.Frame(
        root,
        bg=STONE_DARK
    )

    header.pack(fill="x")

    title = tk.Label(
        header,
        text="âž• ADD MEMORY",
        font=("Segoe UI", 26, "bold"),
        bg=STONE_DARK,
        fg=WHITE
    )

    title.pack(pady=(20, 2))

    subtitle = tk.Label(
        header,
        text="ADD A NEW ITEM TO THE MEMORY VAULT",
        font=("Segoe UI", 10, "bold"),
        bg=STONE_DARK,
        fg=TEAL
    )

    subtitle.pack()

    panel = tk.Frame(
        root,
        bg=STONE,
        highlightbackground=PURPLE_DARK,
        highlightthickness=3
    )

    panel.pack(
        padx=45,
        pady=20,
        fill="both",
        expand=True
    )

    instruction = tk.Label(
        panel,
        text="Enter the memory, idea, prompt or note you want to save:",
        font=("Segoe UI", 11),
        bg=STONE,
        fg=SILVER
    )

    instruction.pack(
        pady=(25, 10)
    )

    text_box = tk.Text(
        panel,
        height=12,
        bg=STONE_LIGHT,
        fg=WHITE,
        insertbackground=WHITE,
        font=("Segoe UI", 11),
        wrap="word",
        relief="flat",
        padx=15,
        pady=15
    )

    text_box.pack(
        padx=50,
        fill="both",
        expand=True
    )

    button_frame = tk.Frame(
        panel,
        bg=STONE
    )

    button_frame.pack(
        pady=15
    )

    save_button = tk.Button(
        button_frame,
        text="ðŸ’¾ SAVE MEMORY",
        command=lambda: save_memory(root, text_box),
        font=("Segoe UI", 11, "bold"),
        bg=PURPLE,
        fg=WHITE,
        activebackground=TEAL,
        activeforeground=STONE_DARK,
        relief="flat",
        padx=25,
        pady=10
    )

    save_button.pack(
        side="left",
        padx=8
    )

    cancel_button = tk.Button(
        button_frame,
        text="â† CANCEL",
        command=lambda: open_memory_vault(root),
        font=("Segoe UI", 11, "bold"),
        bg=STONE_DARK,
        fg=TEAL,
        activebackground=PURPLE,
        activeforeground=WHITE,
        relief="flat",
        padx=25,
        pady=10
    )

    cancel_button.pack(
        side="left",
        padx=8
    )


# ============================================================
# SAVE MEMORY
# ============================================================

def save_memory(root, text_box):

    memory = text_box.get(
        "1.0",
        "end"
    ).strip()

    if not memory:

        messagebox.showwarning(
            "Memory Vault",
            "Please enter something before saving."
        )

        return

    try:

        with open(
            VAULT_PATH,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                "\n" + memory + "\n"
            )

        messagebox.showinfo(
            "Memory Vault",
            "Memory saved successfully."
        )

        open_memory_vault(root)

    except OSError as error:

        messagebox.showerror(
            "Memory Vault",
            f"Could not save memory:\n\n{error}"
        )


# ============================================================
# SEARCH VAULT
# ============================================================

def search_vault(root):

    clear_window(root)

    header = tk.Frame(
        root,
        bg=STONE_DARK
    )

    header.pack(fill="x")

    title = tk.Label(
        header,
        text="ðŸ”Ž SEARCH VAULT",
        font=("Segoe UI", 26, "bold"),
        bg=STONE_DARK,
        fg=WHITE
    )

    title.pack(pady=(20, 2))

    subtitle = tk.Label(
        header,
        text="SEARCH YOUR SAVED NIGHTFORCE MATERIAL",
        font=("Segoe UI", 10, "bold"),
        bg=STONE_DARK,
        fg=TEAL
    )

    subtitle.pack()

    panel = tk.Frame(
        root,
        bg=STONE,
        highlightbackground=PURPLE_DARK,
        highlightthickness=3
    )

    panel.pack(
        padx=45,
        pady=15,
        fill="both",
        expand=True
    )

    back_button = tk.Button(
        panel,
        text="â† RETURN TO MEMORY VAULT",
        command=lambda: open_memory_vault(root),
        font=("Segoe UI", 10, "bold"),
        bg=STONE_DARK,
        fg=TEAL,
        activebackground=PURPLE,
        activeforeground=WHITE,
        relief="flat",
        padx=25,
        pady=8
    )

    back_button.pack(
        side="top",
        anchor="w",
        padx=40,
        pady=(0, 15)
    )


    search_frame = tk.Frame(
        panel,
        bg=STONE
    )

    search_frame.pack(
        fill="x",
        padx=40,
        pady=20
    )

    search_entry = tk.Entry(
        search_frame,
        font=("Segoe UI", 12),
        bg=STONE_LIGHT,
        fg=WHITE,
        insertbackground=WHITE,
        relief="flat"
    )

    search_entry.pack(
        side="left",
        fill="x",
        expand=True,
        ipady=9,
        padx=(0, 10)
    )

    results_box = tk.Text(
        panel,
        bg=STONE_LIGHT,
        fg=WHITE,
        insertbackground=WHITE,
        font=("Segoe UI", 10),
        wrap="word",
        relief="flat",
        padx=15,
        pady=15
    )

    results_box.pack(
        padx=40,
        pady=(0, 15),
        fill="both",
        expand=True
    )

    def perform_search():

        search_term = search_entry.get().strip().lower()

        results_box.config(
            state="normal"
        )

        results_box.delete(
            "1.0",
            "end"
        )

        if not search_term:

            results_box.insert(
                "1.0",
                "Enter a search term above."
            )

            results_box.config(
                state="disabled"
            )

            return

        try:

            with open(
                VAULT_PATH,
                "r",
                encoding="utf-8"
            ) as file:

                lines = file.readlines()

        except FileNotFoundError:

            results_box.insert(
                "1.0",
                "Vault file does not exist yet."
            )

            results_box.config(
                state="disabled"
            )

            return

        matches = []

        for line in lines:

            if search_term in line.lower():

                if line.strip():

                    matches.append(
                        line.strip()
                    )

        if matches:

            results_box.insert(
                "1.0",
                "\n\n".join(matches)
            )

        else:

            results_box.insert(
                "1.0",
                "No matching memories found."
            )

        results_box.config(
            state="disabled"
        )

    search_button = tk.Button(
        search_frame,
        text="SEARCH",
        command=perform_search,
        font=("Segoe UI", 10, "bold"),
        bg=PURPLE,
        fg=WHITE,
        activebackground=TEAL,
        activeforeground=STONE_DARK,
        relief="flat",
        padx=20,
        pady=8
    )

    search_button.pack(
        side="right"
    )

    search_entry.focus_set()


# ============================================================
# MT5 COMMAND ROOM
# ============================================================

def open_mt5_room(root=None):

    if root is None:

        root = tk._default_root

    clear_window(root)

    header = tk.Frame(
        root,
        bg=STONE_DARK
    )

    header.pack(fill="x")

    title = tk.Label(
        header,
        text="ðŸ“ˆ MT5 TRADING BOT",
        font=("Segoe UI", 28, "bold"),
        bg=STONE_DARK,
        fg=WHITE
    )

    title.pack(pady=(25, 2))

    subtitle = tk.Label(
        header,
        text="THE TRADING COMMAND ROOM",
        font=("Segoe UI", 11, "bold"),
        bg=STONE_DARK,
        fg=TEAL
    )

    subtitle.pack()

    room = tk.Frame(
        root,
        bg=STONE,
        highlightbackground=PURPLE_DARK,
        highlightthickness=3
    )

    room.pack(
        padx=45,
        pady=20,
        fill="both",
        expand=True
    )

    warning = tk.Label(
        room,
        text="DEMO / SIMULATION MODE",
        font=("Segoe UI", 14, "bold"),
        bg=STONE_LIGHT,
        fg=TEAL
    )

    warning.pack(pady=(25, 8))

    status = tk.Label(
        room,
        text="Live order execution: DISABLED",
        font=("Segoe UI", 11),
        bg=STONE,
        fg=SILVER
    )

    status.pack(pady=(0, 20))

    signal_button = tk.Button(
        room,
        text="VIEW TRADING SIGNAL",
        command=lambda: show_trading_signal(root),
        font=("Segoe UI", 13, "bold"),
        bg=PURPLE,
        fg=WHITE,
        activebackground=TEAL,
        activeforeground=STONE_DARK,
        relief="flat",
        padx=30,
        pady=12
    )

    signal_button.pack(pady=7)

    account_button = tk.Button(
        room,
        text="ACCOUNT INFORMATION",
        command=lambda: show_account_information(root),
        font=("Segoe UI", 13, "bold"),
        bg=PURPLE,
        fg=WHITE,
        activebackground=TEAL,
        activeforeground=STONE_DARK,
        relief="flat",
        padx=30,
        pady=12
    )

    account_button.pack(pady=7)

    price_button = tk.Button(
        room,
        text="MARKET PRICE",
        command=lambda: show_market_price(root),
        font=("Segoe UI", 13, "bold"),
        bg=PURPLE,
        fg=WHITE,
        activebackground=TEAL,
        activeforeground=STONE_DARK,
        relief="flat",
        padx=30,
        pady=12
    )

    price_button.pack(pady=7)

    safety_button = tk.Button(
        room,
        text="RISK & SAFETY",
        command=lambda: show_risk_safety(root),
        font=("Segoe UI", 13, "bold"),
        bg=STONE_LIGHT,
        fg=TEAL,
        activebackground=PURPLE,
        activeforeground=WHITE,
        relief="flat",
        padx=30,
        pady=12
    )

    safety_button.pack(pady=7)

    back_button = tk.Button(
        room,
        text="â† RETURN TO GREAT HALL",
        command=lambda: show_great_hall(root),
        font=("Segoe UI", 11, "bold"),
        bg=STONE_DARK,
        fg=TEAL,
        activebackground=PURPLE,
        activeforeground=WHITE,
        relief="flat",
        padx=25,
        pady=9
    )

    back_button.pack(pady=(22, 8))


# ============================================================
# TRADING SIGNAL SCREEN
# ============================================================

def show_trading_signal(root):

    clear_window(root)

    header = tk.Frame(root, bg=STONE_DARK)
    header.pack(fill="x")

    title = tk.Label(
        header,
        text="âš” MT5 TRADING SIGNAL",
        font=("Segoe UI", 28, "bold"),
        bg=STONE_DARK,
        fg=WHITE
    )

    title.pack(pady=(25, 2))

    subtitle = tk.Label(
        header,
        text="EURUSD â€¢ M15",
        font=("Segoe UI", 11, "bold"),
        bg=STONE_DARK,
        fg=TEAL
    )

    subtitle.pack()

    panel = tk.Frame(
        root,
        bg=STONE,
        highlightbackground=PURPLE_DARK,
        highlightthickness=3
    )

    panel.pack(
        padx=45,
        pady=20,
        fill="both",
        expand=True
    )

    if not mt5.initialize(MT5_PATH):

        error_label = tk.Label(
            panel,
            text="MT5 CONNECTION FAILED",
            font=("Segoe UI", 22, "bold"),
            bg=STONE,
            fg=TEAL
        )

        error_label.pack(pady=(60, 15))

        detail_label = tk.Label(
            panel,
            text=f"MT5 error: {mt5.last_error()}",
            font=("Segoe UI", 11),
            bg=STONE,
            fg=SILVER
        )

        detail_label.pack(pady=10)

        back_button = tk.Button(
            panel,
            text="â† RETURN TO TRADING COMMAND ROOM",
            command=lambda: open_mt5_room(root),
            font=("Segoe UI", 11, "bold"),
            bg=STONE_DARK,
            fg=TEAL,
            activebackground=PURPLE,
            activeforeground=WHITE,
            relief="flat",
            padx=25,
            pady=10
        )

        back_button.pack(pady=30)

        return

    result = calculate_signal(DEFAULT_SYMBOL)

    signal = result.get(
        "signal",
        "WAIT"
    )

    strength = result.get(
        "strength",
        0
    )

    strength_level = result.get(
        "strength_level",
        "WEAK"
    )

    signal_label = tk.Label(
        panel,
        text=f"SIGNAL: {signal}",
        font=("Segoe UI", 24, "bold"),
        bg=STONE,
        fg=TEAL
    )

    signal_label.pack(
        pady=(30, 5)
    )

    strength_label = tk.Label(
        panel,
        text=f"STRENGTH: {strength}/100  â€¢  {strength_level}",
        font=("Segoe UI", 13, "bold"),
        bg=STONE,
        fg=WHITE
    )

    strength_label.pack(
        pady=(0, 25)
    )

    price = result.get("price")

    if price is not None:

        price_text = f"Current Price: {price}"

    else:

        price_text = "Current Price: unavailable"

    price_label = tk.Label(
        panel,
        text=price_text,
        font=("Segoe UI", 11),
        bg=STONE,
        fg=SILVER
    )

    price_label.pack(pady=4)

    short_average = result.get(
        "short_average"
    )

    long_average = result.get(
        "long_average"
    )

    separation = result.get(
        "average_separation_points",
        0
    )

    averages_text = (
        f"10-Candle Average: {short_average}\n"
        f"30-Candle Average: {long_average}\n"
        f"Separation: {round(separation, 1)} points"
    )

    averages_label = tk.Label(
        panel,
        text=averages_text,
        font=("Segoe UI", 11),
        bg=STONE,
        fg=SILVER,
        justify="center"
    )

    averages_label.pack(
        pady=(15, 20)
    )

    reason_label = tk.Label(
        panel,
        text=f"Reason:\n{result.get('reason', 'No reason available.')}",
        font=("Segoe UI", 11),
        bg=STONE_LIGHT,
        fg=WHITE,
        wraplength=750,
        justify="center",
        padx=20,
        pady=15
    )

    reason_label.pack(
        padx=30,
        fill="x"
    )

    conditions = result.get(
        "conditions",
        []
    )

    conditions_text = "\n".join(
        conditions
    )

    conditions_label = tk.Label(
        panel,
        text=f"Conditions:\n{conditions_text}",
        font=("Segoe UI", 10),
        bg=STONE,
        fg=TEAL,
        justify="left"
    )

    conditions_label.pack(
        pady=(20, 10)
    )

    warning_label = tk.Label(
        panel,
        text="âš  SIGNAL ONLY â€¢ NO ORDER HAS BEEN CREATED",
        font=("Segoe UI", 10, "bold"),
        bg=STONE,
        fg=PURPLE
    )

    warning_label.pack(
        pady=10
    )

    back_button = tk.Button(
        panel,
        text="â† RETURN TO TRADING COMMAND ROOM",
        command=lambda: (
            mt5.shutdown(),
            open_mt5_room(root)
        ),
        font=("Segoe UI", 11, "bold"),
        bg=STONE_DARK,
        fg=TEAL,
        activebackground=PURPLE,
        activeforeground=WHITE,
        relief="flat",
        padx=25,
        pady=10
    )

    back_button.pack(
        pady=(15, 25)
    )


# ============================================================
# ACCOUNT INFORMATION SCREEN
# ============================================================

def show_account_information(root):

    clear_window(root)

    header = tk.Frame(root, bg=STONE_DARK)
    header.pack(fill="x")

    title = tk.Label(
        header,
        text="ðŸ‘¤ MT5 ACCOUNT INFORMATION",
        font=("Segoe UI", 28, "bold"),
        bg=STONE_DARK,
        fg=WHITE
    )

    title.pack(pady=(25, 2))

    subtitle = tk.Label(
        header,
        text="DEMO ACCOUNT",
        font=("Segoe UI", 11, "bold"),
        bg=STONE_DARK,
        fg=TEAL
    )

    subtitle.pack()

    panel = tk.Frame(
        root,
        bg=STONE,
        highlightbackground=PURPLE_DARK,
        highlightthickness=3
    )

    panel.pack(
        padx=45,
        pady=20,
        fill="both",
        expand=True
    )

    if not mt5.initialize(MT5_PATH):

        error_label = tk.Label(
            panel,
            text="MT5 CONNECTION FAILED",
            font=("Segoe UI", 22, "bold"),
            bg=STONE,
            fg=TEAL
        )

        error_label.pack(pady=(60, 15))

        detail_label = tk.Label(
            panel,
            text=f"MT5 error: {mt5.last_error()}",
            font=("Segoe UI", 11),
            bg=STONE,
            fg=SILVER
        )

        detail_label.pack(pady=10)

        back_button = tk.Button(
            panel,
            text="â† RETURN TO TRADING COMMAND ROOM",
            command=lambda: open_mt5_room(root),
            font=("Segoe UI", 11, "bold"),
            bg=STONE_DARK,
            fg=TEAL,
            activebackground=PURPLE,
            activeforeground=WHITE,
            relief="flat",
            padx=25,
            pady=10
        )

        back_button.pack(pady=30)

        return

    account = mt5.account_info()

    if account is None:

        error_label = tk.Label(
            panel,
            text="ACCOUNT INFORMATION UNAVAILABLE",
            font=("Segoe UI", 22, "bold"),
            bg=STONE,
            fg=TEAL
        )

        error_label.pack(pady=(60, 15))

        detail_label = tk.Label(
            panel,
            text=f"MT5 error: {mt5.last_error()}",
            font=("Segoe UI", 11),
            bg=STONE,
            fg=SILVER
        )

        detail_label.pack(pady=10)

    else:

        account_title = tk.Label(
            panel,
            text="CONNECTED DEMO ACCOUNT",
            font=("Segoe UI", 20, "bold"),
            bg=STONE,
            fg=TEAL
        )

        account_title.pack(
            pady=(35, 25)
        )

        account_text = (
            f"Login: {account.login}\n\n"
            f"Server: {account.server}\n\n"
            f"Balance: {account.balance:.2f} {account.currency}\n\n"
            f"Equity: {account.equity:.2f} {account.currency}\n\n"
            f"Currency: {account.currency}"
        )

        account_label = tk.Label(
            panel,
            text=account_text,
            font=("Segoe UI", 13),
            bg=STONE_LIGHT,
            fg=WHITE,
            justify="center",
            padx=40,
            pady=25
        )

        account_label.pack(
            padx=100,
            fill="x"
        )

        safety_label = tk.Label(
            panel,
            text="âœ“ ACCOUNT INFORMATION ONLY â€¢ NO TRADES CREATED",
            font=("Segoe UI", 10, "bold"),
            bg=STONE,
            fg=PURPLE
        )

        safety_label.pack(
            pady=20
        )

    back_button = tk.Button(
        panel,
        text="â† RETURN TO TRADING COMMAND ROOM",
        command=lambda: (
            mt5.shutdown(),
            open_mt5_room(root)
        ),
        font=("Segoe UI", 11, "bold"),
        bg=STONE_DARK,
        fg=TEAL,
        activebackground=PURPLE,
        activeforeground=WHITE,
        relief="flat",
        padx=25,
        pady=10
    )

    back_button.pack(
        pady=(15, 25)
    )


# ============================================================
# MARKET PRICE SCREEN
# ============================================================

def show_market_price(root):

    clear_window(root)

    header = tk.Frame(root, bg=STONE_DARK)
    header.pack(fill="x")

    title = tk.Label(
        header,
        text="ðŸ’¹ MT5 MARKET PRICE",
        font=("Segoe UI", 28, "bold"),
        bg=STONE_DARK,
        fg=WHITE
    )

    title.pack(pady=(25, 2))

    subtitle = tk.Label(
        header,
        text=f"{DEFAULT_SYMBOL} â€¢ LIVE MARKET DATA",
        font=("Segoe UI", 11, "bold"),
        bg=STONE_DARK,
        fg=TEAL
    )

    subtitle.pack()

    panel = tk.Frame(
        root,
        bg=STONE,
        highlightbackground=PURPLE_DARK,
        highlightthickness=3
    )

    panel.pack(
        padx=45,
        pady=20,
        fill="both",
        expand=True
    )

    if not mt5.initialize(MT5_PATH):

        error_label = tk.Label(
            panel,
            text="MT5 CONNECTION FAILED",
            font=("Segoe UI", 22, "bold"),
            bg=STONE,
            fg=TEAL
        )

        error_label.pack(pady=(60, 15))

        detail_label = tk.Label(
            panel,
            text=f"MT5 error: {mt5.last_error()}",
            font=("Segoe UI", 11),
            bg=STONE,
            fg=SILVER
        )

        detail_label.pack(pady=10)

        back_button = tk.Button(
            panel,
            text="â† RETURN TO TRADING COMMAND ROOM",
            command=lambda: open_mt5_room(root),
            font=("Segoe UI", 11, "bold"),
            bg=STONE_DARK,
            fg=TEAL,
            activebackground=PURPLE,
            activeforeground=WHITE,
            relief="flat",
            padx=25,
            pady=10
        )

        back_button.pack(pady=30)

        return

    symbol_info = mt5.symbol_info_tick(
        DEFAULT_SYMBOL
    )

    if symbol_info is None:

        error_label = tk.Label(
            panel,
            text="MARKET PRICE UNAVAILABLE",
            font=("Segoe UI", 22, "bold"),
            bg=STONE,
            fg=TEAL
        )

        error_label.pack(pady=(60, 15))

        detail_label = tk.Label(
            panel,
            text=f"MT5 error: {mt5.last_error()}",
            font=("Segoe UI", 11),
            bg=STONE,
            fg=SILVER
        )

        detail_label.pack(pady=10)

    else:

        bid = float(symbol_info.bid)
        ask = float(symbol_info.ask)
        spread = ask - bid

        price_title = tk.Label(
            panel,
            text=DEFAULT_SYMBOL,
            font=("Segoe UI", 26, "bold"),
            bg=STONE,
            fg=TEAL
        )

        price_title.pack(
            pady=(35, 25)
        )

        price_frame = tk.Frame(
            panel,
            bg=STONE_LIGHT,
            highlightbackground=PURPLE,
            highlightthickness=2
        )

        price_frame.pack(
            padx=100,
            fill="x"
        )

        bid_label = tk.Label(
            price_frame,
            text=f"BID\n{bid:.5f}",
            font=("Segoe UI", 18, "bold"),
            bg=STONE_LIGHT,
            fg=WHITE
        )

        bid_label.grid(
            row=0,
            column=0,
            padx=50,
            pady=25
        )

        ask_label = tk.Label(
            price_frame,
            text=f"ASK\n{ask:.5f}",
            font=("Segoe UI", 18, "bold"),
            bg=STONE_LIGHT,
            fg=WHITE
        )

        ask_label.grid(
            row=0,
            column=1,
            padx=50,
            pady=25
        )

        spread_label = tk.Label(
            price_frame,
            text=f"SPREAD\n{spread:.5f}",
            font=("Segoe UI", 18, "bold"),
            bg=STONE_LIGHT,
            fg=TEAL
        )

        spread_label.grid(
            row=0,
            column=2,
            padx=50,
            pady=25
        )

        price_frame.columnconfigure(
            0,
            weight=1
        )

        price_frame.columnconfigure(
            1,
            weight=1
        )

        price_frame.columnconfigure(
            2,
            weight=1
        )

        status_label = tk.Label(
            panel,
            text="âœ“ MT5 CONNECTED â€¢ MARKET DATA RECEIVED",
            font=("Segoe UI", 11, "bold"),
            bg=STONE,
            fg=TEAL
        )

        status_label.pack(
            pady=(25, 10)
        )

        safety_label = tk.Label(
            panel,
            text="âœ“ MARKET DATA ONLY â€¢ NO TRADES CREATED",
            font=("Segoe UI", 10, "bold"),
            bg=STONE,
            fg=PURPLE
        )

        safety_label.pack(
            pady=10
        )

    back_button = tk.Button(
        panel,
        text="â† RETURN TO TRADING COMMAND ROOM",
        command=lambda: (
            mt5.shutdown(),
            open_mt5_room(root)
        ),
        font=("Segoe UI", 11, "bold"),
        bg=STONE_DARK,
        fg=TEAL,
        activebackground=PURPLE,
        activeforeground=WHITE,
        relief="flat",
        padx=25,
        pady=10
    )

    back_button.pack(
        pady=(20, 25)
    )


# ============================================================
# RISK & SAFETY SCREEN
# ============================================================

def show_risk_safety(root):

    clear_window(root)

    header = tk.Frame(
        root,
        bg=STONE_DARK
    )

    header.pack(fill="x")

    title = tk.Label(
        header,
        text="ðŸ›¡ MT5 RISK & SAFETY",
        font=("Segoe UI", 24, "bold"),
        bg=STONE_DARK,
        fg=WHITE
    )

    title.pack(pady=(18, 2))

    subtitle = tk.Label(
        header,
        text="TRADING PROTECTION SETTINGS",
        font=("Segoe UI", 10, "bold"),
        bg=STONE_DARK,
        fg=TEAL
    )

    subtitle.pack()

    panel = tk.Frame(
        root,
        bg=STONE,
        highlightbackground=PURPLE_DARK,
        highlightthickness=3
    )

    panel.pack(
        padx=45,
        pady=15,
        fill="both",
        expand=True
    )

    mode_label = tk.Label(
        panel,
        text="TRADING MODE",
        font=("Segoe UI", 10, "bold"),
        bg=STONE,
        fg=TEAL
    )

    mode_label.pack(
        pady=(12, 2)
    )

    mode_value = tk.Label(
        panel,
        text="DEMO / SIMULATION",
        font=("Segoe UI", 16, "bold"),
        bg=STONE_LIGHT,
        fg=WHITE,
        padx=30,
        pady=6
    )

    mode_value.pack()

    live_label = tk.Label(
        panel,
        text="LIVE ORDER EXECUTION",
        font=("Segoe UI", 10, "bold"),
        bg=STONE,
        fg=TEAL
    )

    live_label.pack(
        pady=(10, 2)
    )

    live_value = tk.Label(
        panel,
        text="DISABLED",
        font=("Segoe UI", 16, "bold"),
        bg=STONE_LIGHT,
        fg=WHITE,
        padx=30,
        pady=6
    )

    live_value.pack()

    settings_frame = tk.Frame(
        panel,
        bg=STONE_LIGHT,
        highlightbackground=PURPLE,
        highlightthickness=2
    )

    settings_frame.pack(
        padx=100,
        pady=12,
        fill="x"
    )

    risk_label = tk.Label(
        settings_frame,
        text=f"Risk per trade: {DEFAULT_RISK_PERCENT}%",
        font=("Segoe UI", 11),
        bg=STONE_LIGHT,
        fg=WHITE
    )

    risk_label.pack(pady=5)

    lot_label = tk.Label(
        settings_frame,
        text=f"Maximum lot size: {DEFAULT_MAX_LOT}",
        font=("Segoe UI", 11),
        bg=STONE_LIGHT,
        fg=WHITE
    )

    lot_label.pack(pady=5)

    stop_label = tk.Label(
        settings_frame,
        text=f"Required stop-loss: {DEFAULT_STOP_LOSS_POINTS} points",
        font=("Segoe UI", 11),
        bg=STONE_LIGHT,
        fg=WHITE
    )

    stop_label.pack(pady=5)

    symbol_label = tk.Label(
        settings_frame,
        text=f"Default symbol: {DEFAULT_SYMBOL}",
        font=("Segoe UI", 11),
        bg=STONE_LIGHT,
        fg=WHITE
    )

    symbol_label.pack(pady=5)

    safety_text = (
        "âœ“ Live order execution is not implemented\n"
        "âœ“ Current system is signal-only\n"
        "âœ“ Risk settings are display-only\n"
        "âœ“ No trade can be created from this screen"
    )

    safety_label = tk.Label(
        panel,
        text=safety_text,
        font=("Segoe UI", 10),
        bg=STONE,
        fg=TEAL,
        justify="left"
    )

    safety_label.pack(
        pady=(4, 6)
    )

    warning_label = tk.Label(
        panel,
        text="âš  SAFETY FIRST â€¢ DEMO / SIMULATION ONLY",
        font=("Segoe UI", 10, "bold"),
        bg=STONE,
        fg=PURPLE
    )

    warning_label.pack(
        pady=5
    )

    back_button = tk.Button(
        panel,
        text="â† RETURN TO TRADING COMMAND ROOM",
        command=lambda: open_mt5_room(root),
        font=("Segoe UI", 10, "bold"),
        bg=STONE_DARK,
        fg=TEAL,
        activebackground=PURPLE,
        activeforeground=WHITE,
        relief="flat",
        padx=25,
        pady=8
    )

    back_button.pack(
        side="top",
        anchor="w",
        padx=40,
        pady=(10, 5)
    )


# ============================================================
# CLEAR CURRENT SCREEN
# ============================================================

def clear_window(root):

    for widget in root.winfo_children():

        widget.destroy()


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    launch_castle()




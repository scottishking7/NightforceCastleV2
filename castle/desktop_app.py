import tkinter as tk
import MetaTrader5 as mt5

from castle.signal_engine import calculate_signal


WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 700

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"
DEFAULT_SYMBOL = "EURUSD"

DEFAULT_RISK_PERCENT = 1.0
DEFAULT_MAX_LOT = 0.10
DEFAULT_STOP_LOSS_POINTS = 200


# ============================================================
# COLOUR PALETTE
# ============================================================

STONE_DARK = "#090B14"
STONE = "#111522"
STONE_LIGHT = "#1B2030"

PURPLE = "#6C4AB6"
PURPLE_DARK = "#3D286B"

TEAL = "#19D3C5"
SILVER = "#B8C0D0"
WHITE = "#F2F2F2"


# ============================================================
# MAIN CASTLE WINDOW
# ============================================================

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

    header = tk.Frame(root, bg=STONE_DARK)
    header.pack(fill="x")

    title = tk.Label(
        header,
        text="🏰 NIGHTFORCE CASTLE",
        font=("Segoe UI", 28, "bold"),
        bg=STONE_DARK,
        fg=WHITE
    )

    title.pack(pady=(25, 2))

    subtitle = tk.Label(
        header,
        text="THE GREAT HALL",
        font=("Segoe UI", 11, "bold"),
        bg=STONE_DARK,
        fg=TEAL
    )

    subtitle.pack()

    hall = tk.Frame(
        root,
        bg=STONE,
        highlightbackground=PURPLE_DARK,
        highlightthickness=3
    )

    hall.pack(
        padx=45,
        pady=20,
        fill="both",
        expand=True
    )

    command_frame = tk.Frame(
        hall,
        bg=STONE_LIGHT,
        highlightbackground=PURPLE,
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
        bg=STONE_LIGHT,
        fg=WHITE
    )

    command_title.pack(pady=(18, 4))

    command_text = tk.Label(
        command_frame,
        text="The heart of Nightforce Castle",
        font=("Segoe UI", 11),
        bg=STONE_LIGHT,
        fg=TEAL
    )

    command_text.pack(pady=(0, 18))

    rooms = tk.Frame(hall, bg=STONE)

    rooms.pack(
        padx=35,
        pady=5,
        fill="both",
        expand=True
    )

    room_data = [
        ("📈", "MT5 TRADING BOT", open_mt5_room),
        ("📚", "MEMORY VAULT", None),
        ("🖼️", "IMAGE WORKSHOP", None),
        ("✨", "SOCIAL STUDIO", None),
        ("🔎", "RESEARCH AGENT", None),
        ("📻", "MIDNIGHT RADIO", None),
        ("⚙️", "SETTINGS", None),
        ("🚪", "EXIT CASTLE", root.destroy)
    ]

    for index, (icon, name, command) in enumerate(room_data):

        row = index // 4
        column = index % 4

        room = tk.Frame(
            rooms,
            bg=STONE_LIGHT,
            highlightbackground=PURPLE_DARK,
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
            bg=STONE_LIGHT,
            fg=WHITE
        )

        icon_label.pack(pady=(14, 4))

        if command is not None:

            button = tk.Button(
                room,
                text=name,
                command=command,
                font=("Segoe UI", 9, "bold"),
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
                font=("Segoe UI", 9, "bold"),
                bg=STONE_LIGHT,
                fg=SILVER
            )

            name_label.pack(pady=(0, 14))

    for column in range(4):
        rooms.columnconfigure(column, weight=1)

    for row in range(2):
        rooms.rowconfigure(row, weight=1)

    footer = tk.Label(
        hall,
        text="NIGHTFORCE CASTLE  •  PRIVATE COMMAND CENTRE",
        font=("Segoe UI", 9),
        bg=STONE,
        fg=PURPLE
    )

    footer.pack(pady=(5, 18))


# ============================================================
# MT5 COMMAND ROOM
# ============================================================

def open_mt5_room(root=None):

    if root is None:
        root = tk._default_root

    clear_window(root)

    header = tk.Frame(root, bg=STONE_DARK)
    header.pack(fill="x")

    title = tk.Label(
        header,
        text="📈 MT5 TRADING BOT",
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
        text="← RETURN TO GREAT HALL",
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
        text="⚔ MT5 TRADING SIGNAL",
        font=("Segoe UI", 28, "bold"),
        bg=STONE_DARK,
        fg=WHITE
    )

    title.pack(pady=(25, 2))

    subtitle = tk.Label(
        header,
        text="EURUSD • M15",
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
            text="← RETURN TO TRADING COMMAND ROOM",
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

    signal = result.get("signal", "WAIT")
    strength = result.get("strength", 0)
    strength_level = result.get("strength_level", "WEAK")

    signal_label = tk.Label(
        panel,
        text=f"SIGNAL: {signal}",
        font=("Segoe UI", 24, "bold"),
        bg=STONE,
        fg=TEAL
    )

    signal_label.pack(pady=(30, 5))

    strength_label = tk.Label(
        panel,
        text=f"STRENGTH: {strength}/100  •  {strength_level}",
        font=("Segoe UI", 13, "bold"),
        bg=STONE,
        fg=WHITE
    )

    strength_label.pack(pady=(0, 25))

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

    short_average = result.get("short_average")
    long_average = result.get("long_average")
    separation = result.get("average_separation_points", 0)

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

    averages_label.pack(pady=(15, 20))

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

    conditions = result.get("conditions", [])

    conditions_label = tk.Label(
        panel,
        text=f"Conditions:\n{chr(10).join(conditions)}",
        font=("Segoe UI", 10),
        bg=STONE,
        fg=TEAL,
        justify="left"
    )

    conditions_label.pack(pady=(20, 10))

    warning_label = tk.Label(
        panel,
        text="⚠ SIGNAL ONLY • NO ORDER HAS BEEN CREATED",
        font=("Segoe UI", 10, "bold"),
        bg=STONE,
        fg=PURPLE
    )

    warning_label.pack(pady=10)

    back_button = tk.Button(
        panel,
        text="← RETURN TO TRADING COMMAND ROOM",
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

    back_button.pack(pady=(15, 25))


# ============================================================
# ACCOUNT INFORMATION SCREEN
# ============================================================

def show_account_information(root):

    clear_window(root)

    header = tk.Frame(root, bg=STONE_DARK)
    header.pack(fill="x")

    title = tk.Label(
        header,
        text="👤 MT5 ACCOUNT INFORMATION",
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
            text="← RETURN TO TRADING COMMAND ROOM",
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

        account_title.pack(pady=(35, 25))

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
            text="✓ ACCOUNT INFORMATION ONLY • NO TRADES CREATED",
            font=("Segoe UI", 10, "bold"),
            bg=STONE,
            fg=PURPLE
        )

        safety_label.pack(pady=20)

    back_button = tk.Button(
        panel,
        text="← RETURN TO TRADING COMMAND ROOM",
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

    back_button.pack(pady=(15, 25))


# ============================================================
# MARKET PRICE SCREEN
# ============================================================

def show_market_price(root):

    clear_window(root)

    header = tk.Frame(root, bg=STONE_DARK)
    header.pack(fill="x")

    title = tk.Label(
        header,
        text="💹 MT5 MARKET PRICE",
        font=("Segoe UI", 28, "bold"),
        bg=STONE_DARK,
        fg=WHITE
    )

    title.pack(pady=(25, 2))

    subtitle = tk.Label(
        header,
        text=f"{DEFAULT_SYMBOL} • LIVE MARKET DATA",
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
            text="← RETURN TO TRADING COMMAND ROOM",
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

    symbol_info = mt5.symbol_info_tick(DEFAULT_SYMBOL)

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

        price_title.pack(pady=(35, 25))

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

        price_frame.columnconfigure(0, weight=1)
        price_frame.columnconfigure(1, weight=1)
        price_frame.columnconfigure(2, weight=1)

        status_label = tk.Label(
            panel,
            text="✓ MT5 CONNECTED • MARKET DATA RECEIVED",
            font=("Segoe UI", 11, "bold"),
            bg=STONE,
            fg=TEAL
        )

        status_label.pack(pady=(25, 10))

        safety_label = tk.Label(
            panel,
            text="✓ MARKET DATA ONLY • NO TRADES CREATED",
            font=("Segoe UI", 10, "bold"),
            bg=STONE,
            fg=PURPLE
        )

        safety_label.pack(pady=10)

    back_button = tk.Button(
        panel,
        text="← RETURN TO TRADING COMMAND ROOM",
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

    back_button.pack(pady=(20, 25))


# ============================================================
# RISK & SAFETY SCREEN
# ============================================================

def show_risk_safety(root):

    clear_window(root)

    header = tk.Frame(root, bg=STONE_DARK)
    header.pack(fill="x")

    title = tk.Label(
        header,
        text="🛡 MT5 RISK & SAFETY",
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

    mode_label.pack(pady=(12, 2))

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

    live_label.pack(pady=(10, 2))

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
        "✓ Live order execution is not implemented\n"
        "✓ Current system is signal-only\n"
        "✓ Risk settings are display-only\n"
        "✓ No trade can be created from this screen"
    )

    safety_label = tk.Label(
        panel,
        text=safety_text,
        font=("Segoe UI", 10),
        bg=STONE,
        fg=TEAL,
        justify="left"
    )

    safety_label.pack(pady=(4, 6))

    warning_label = tk.Label(
        panel,
        text="⚠ SAFETY FIRST • DEMO / SIMULATION ONLY",
        font=("Segoe UI", 10, "bold"),
        bg=STONE,
        fg=PURPLE
    )

    warning_label.pack(pady=5)

    back_button = tk.Button(
        panel,
        text="← RETURN TO TRADING COMMAND ROOM",
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

    back_button.pack(pady=(8, 15))


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
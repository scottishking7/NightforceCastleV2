import MetaTrader5 as mt5
from castle.signal_engine import calculate_signal

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"

DEFAULT_SYMBOL = "EURUSD"
DEFAULT_RISK_PERCENT = 1.0
DEFAULT_MAX_LOT = 0.10
DEFAULT_STOP_LOSS_POINTS = 200


def trading_bot():

    while True:

        print()
        print("=" * 70)
        print("📈 MT5 TRADING BOT")
        print("=" * 70)
        print()

        print("1 - MT5 Connection Status")
        print("2 - Account Information")
        print("3 - Market Price")
        print("4 - Trading Signal")
        print("5 - Risk Settings")
        print("6 - Return")
        print()

        choice = input("Choose: ")

        print()

        if choice == "1":

            show_connection_status()

        elif choice == "2":

            show_account_information()

        elif choice == "3":

            show_market_price()

        elif choice == "4":

            show_trading_signal()

        elif choice == "5":

            show_risk_settings()

        elif choice == "6":

            return



        else:

            print("❌ Invalid option.")
            input("\nPress Enter to continue...")


def show_connection_status():

    print("=" * 70)
    print("MT5 CONNECTION")
    print("=" * 70)
    print()

    initialized = mt5.initialize(MT5_PATH)

    print(
        "Connection:",
        "CONNECTED" if initialized else "FAILED"
    )

    print(
        "Last Error:",
        mt5.last_error()
    )

    print()

    if initialized:

        terminal = mt5.terminal_info()

        if terminal:

            print("Terminal Connected: Yes")
            print(
                "Trade Allowed:",
                terminal.trade_allowed
            )

        mt5.shutdown()

    print()
    input("Press Enter to continue...")


def show_account_information():

    print("=" * 70)
    print("MT5 ACCOUNT INFORMATION")
    print("=" * 70)
    print()

    initialized = mt5.initialize(MT5_PATH)

    if not initialized:

        print("❌ Unable to connect to MT5.")
        print("Last Error:", mt5.last_error())
        print()
        input("Press Enter to continue...")
        return

    account = mt5.account_info()

    if account:

        print("Login:", account.login)
        print("Server:", account.server)
        print("Currency:", account.currency)
        print("Balance:", account.balance)
        print("Equity:", account.equity)
        print("Margin:", account.margin)
        print("Free Margin:", account.margin_free)

    else:

        print("❌ Unable to read account information.")
        print("Last Error:", mt5.last_error())

    mt5.shutdown()

    print()
    input("Press Enter to continue...")


def show_market_price():

    print("=" * 70)
    print("MT5 MARKET PRICE")
    print("=" * 70)
    print()

    symbol = input(
        f"Enter symbol (default {DEFAULT_SYMBOL}): "
    ).strip().upper()

    if not symbol:

        symbol = DEFAULT_SYMBOL

    initialized = mt5.initialize(MT5_PATH)

    if not initialized:

        print("❌ Unable to connect to MT5.")
        print("Last Error:", mt5.last_error())
        print()
        input("Press Enter to continue...")
        return

    symbol_info = mt5.symbol_info(symbol)

    if symbol_info is None:

        print(f"❌ Symbol not found: {symbol}")
        print("Last Error:", mt5.last_error())

        mt5.shutdown()

        print()
        input("Press Enter to continue...")
        return

    if not symbol_info.visible:

        mt5.symbol_select(symbol, True)

    tick = mt5.symbol_info_tick(symbol)

    if tick is None:

        print(f"❌ Unable to read market price for {symbol}.")
        print("Last Error:", mt5.last_error())

    else:

        print()
        print("Symbol:", symbol)
        print("Bid:", tick.bid)
        print("Ask:", tick.ask)
        print("Last:", tick.last)

    mt5.shutdown()

    print()
    input("Press Enter to continue...")


def show_risk_settings():

    print("=" * 70)
    print("TRADING RISK SETTINGS")
    print("=" * 70)
    print()

    print("Trading mode: DEMO / SIMULATION")
    print("Live order execution: DISABLED")
    print()

    print(
        "Default symbol:",
        DEFAULT_SYMBOL
    )

    print(
        "Risk per trade:",
        f"{DEFAULT_RISK_PERCENT}%"
    )

    print(
        "Maximum lot size:",
        DEFAULT_MAX_LOT
    )

    print(
        "Required stop-loss:",
        f"{DEFAULT_STOP_LOSS_POINTS} points"
    )

    print()

    print("Safety rules:")
    print("✓ Live order execution is not implemented")
    print("✓ Risk is capped by the maximum lot setting")
    print("✓ Stop-loss is required for future trade logic")
    print("✓ Strategy signals will be added separately")

    print()
    input("Press Enter to continue...")

def show_trading_signal():

    print("=" * 70)
    print("MT5 TRADING SIGNAL")
    print("=" * 70)
    print()

    symbol = input(
        f"Enter symbol (default {DEFAULT_SYMBOL}): "
    ).strip().upper()

    if not symbol:
        symbol = DEFAULT_SYMBOL

    initialized = mt5.initialize(MT5_PATH)

    if not initialized:
        print("Unable to connect to MT5.")
        print("Last Error:", mt5.last_error())
        print()
        input("Press Enter to continue...")
        return

    symbol_info = mt5.symbol_info(symbol)

    if symbol_info is None:
        print(f"Symbol not found: {symbol}")
        print("Last Error:", mt5.last_error())
        mt5.shutdown()
        print()
        input("Press Enter to continue...")
        return

    if not symbol_info.visible:
        mt5.symbol_select(symbol, True)

    result = calculate_signal(symbol)

    print()
    print("Symbol:", symbol)
    print("Timeframe: M15")
    print()
    print("Signal:", result.get("signal"))
    print()
    print("Reason:")
    print(result.get("reason"))

    if result.get("price") is not None:
        print()
        print("Current Price:", result.get("price"))
        print("10-Candle Average:", result.get("short_average"))
        print("30-Candle Average:", result.get("long_average"))

    print()
    print("WARNING: SIGNAL ONLY")
    print("NO ORDER HAS BEEN CREATED.")
    print()

    mt5.shutdown()

    input("Press Enter to continue...")
if __name__ == "__main__":

    trading_bot()

import MetaTrader5 as mt5


MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"


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
        print("4 - Return")
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

    symbol = input("Enter symbol (example: EURUSD): ").strip().upper()

    if not symbol:

        print("❌ No symbol entered.")
        input("\nPress Enter to continue...")
        return

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


if __name__ == "__main__":

    trading_bot()
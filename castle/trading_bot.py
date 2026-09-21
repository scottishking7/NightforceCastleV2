import time

import MetaTrader5 as mt5
from castle.signal_engine import calculate_signal

MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"

DEFAULT_SYMBOL = "EURUSD"
DEFAULT_RISK_PERCENT = 1.0
DEFAULT_MAX_LOT = 0.10
DEFAULT_STOP_LOSS_POINTS = 200
FIRST_DEMO_MAX_LOT = 0.01
TICK_ACTIVITY_TIMEOUT_SECONDS = 5.0
TICK_ACTIVITY_POLL_SECONDS = 0.5
MAX_TICK_ADVANCE_SECONDS = 10.0
POSITION_VERIFICATION_ATTEMPTS = 5
POSITION_VERIFICATION_DELAY_SECONDS = 0.2
CASTLE_MAGIC_NUMBER = 26092026
DEMO_EXECUTION_ARM_TOKEN = "ARM_DEMO_EXECUTION"


def require_demo_execution_armed(arm_token):

    if arm_token != DEMO_EXECUTION_ARM_TOKEN:
        raise ValueError(
            "Execution blocked: demo execution is not explicitly armed."
        )

    return True


def require_demo_account():

    account = mt5.account_info()

    if account is None:
        return False, "Could not retrieve MT5 account information."

    if account.trade_mode != mt5.ACCOUNT_TRADE_MODE_DEMO:
        return (
            False,
            "Execution blocked: MT5 account is not a demo account.",
        )

    return True, "Demo account verified."


def require_demo_execution_environment(symbol=DEFAULT_SYMBOL):

    terminal = mt5.terminal_info()
    account = mt5.account_info()
    symbol_info = mt5.symbol_info(symbol)

    if terminal is None:
        return False, "Execution blocked: MT5 terminal information unavailable."

    if account is None:
        return False, "Execution blocked: MT5 account information unavailable."

    if symbol_info is None:
        return False, f"Execution blocked: symbol unavailable: {symbol}"

    if not terminal.trade_allowed:
        return False, "Execution blocked: MT5 Algo Trading is disabled."

    if terminal.tradeapi_disabled:
        return False, "Execution blocked: MT5 Python trading API is disabled."

    if account.trade_mode != mt5.ACCOUNT_TRADE_MODE_DEMO:
        return False, "Execution blocked: MT5 account is not a demo account."

    if not account.trade_allowed:
        return False, "Execution blocked: account trading is not allowed."

    if not account.trade_expert:
        return False, "Execution blocked: Expert Advisor trading is not allowed."

    if symbol_info.trade_mode != mt5.SYMBOL_TRADE_MODE_FULL:
        return False, f"Execution blocked: full trading is not enabled for {symbol}."

    return True, "Demo execution environment verified."


def require_no_open_castle_position(symbol=DEFAULT_SYMBOL):

    positions = mt5.positions_get(symbol=symbol)

    if positions is None:
        return (
            False,
            f"Execution blocked: could not retrieve open positions for {symbol}.",
        )

    castle_positions = [
        position
        for position in positions
        if position.magic == CASTLE_MAGIC_NUMBER
    ]

    if castle_positions:
        return (
            False,
            f"Execution blocked: Castle already has an open {symbol} position.",
        )

    return True, f"No open Castle position found for {symbol}."


def get_open_castle_position(symbol=DEFAULT_SYMBOL):

    positions = mt5.positions_get(symbol=symbol)

    if positions is None:
        raise ValueError(
            f"Could not retrieve open positions for {symbol}."
        )

    castle_positions = [
        position
        for position in positions
        if position.magic == CASTLE_MAGIC_NUMBER
    ]

    if not castle_positions:
        raise ValueError(
            f"No open Castle position found for {symbol}."
        )

    if len(castle_positions) != 1:
        raise ValueError(
            f"Expected exactly one Castle position for {symbol}; "
            f"found {len(castle_positions)}."
        )

    return castle_positions[0]


def retry_position_verification(
    verification_function,
    *args,
    attempts=POSITION_VERIFICATION_ATTEMPTS,
    delay_seconds=POSITION_VERIFICATION_DELAY_SECONDS,
):

    if attempts <= 0:
        raise ValueError(
            "Position verification attempts must be greater than zero."
        )

    if delay_seconds < 0:
        raise ValueError(
            "Position verification delay cannot be negative."
        )

    last_error = None

    for attempt in range(attempts):
        try:
            return verification_function(*args)

        except ValueError as exc:
            last_error = exc

            if attempt < attempts - 1:
                time.sleep(delay_seconds)

    raise last_error


def verify_open_castle_position(
    request,
):

    position = get_open_castle_position(request["symbol"])

    if position.symbol != request["symbol"]:
        raise ValueError(
            "Post-execution verification failed: "
            "position symbol does not match request."
        )

    if position.magic != CASTLE_MAGIC_NUMBER:
        raise ValueError(
            "Post-execution verification failed: "
            "position magic number does not match Castle."
        )

    if position.type != request["type"]:
        raise ValueError(
            "Post-execution verification failed: "
            "position direction does not match request."
        )

    if abs(position.volume - request["volume"]) > 1e-8:
        raise ValueError(
            "Post-execution verification failed: "
            "position volume does not match request."
        )

    return position


def verify_closed_castle_position(
    symbol=DEFAULT_SYMBOL,
):

    positions = mt5.positions_get(symbol=symbol)

    if positions is None:
        raise ValueError(
            "Post-close verification failed: "
            f"could not retrieve open positions for {symbol}."
        )

    castle_positions = [
        position
        for position in positions
        if position.magic == CASTLE_MAGIC_NUMBER
    ]

    if castle_positions:
        raise ValueError(
            "Post-close verification failed: "
            f"Castle position still open for {symbol}."
        )

    return True


def require_fresh_market_tick(
    symbol=DEFAULT_SYMBOL,
    timeout_seconds=TICK_ACTIVITY_TIMEOUT_SECONDS,
    poll_seconds=TICK_ACTIVITY_POLL_SECONDS,
    max_advance_seconds=MAX_TICK_ADVANCE_SECONDS,
):

    if timeout_seconds <= 0:
        raise ValueError(
            "Tick activity timeout must be greater than zero."
        )

    if poll_seconds <= 0:
        raise ValueError(
            "Tick activity poll interval must be greater than zero."
        )

    if max_advance_seconds <= 0:
        raise ValueError(
            "Maximum tick advance must be greater than zero."
        )

    first_tick = mt5.symbol_info_tick(symbol)

    if first_tick is None:
        raise ValueError(
            f"Could not retrieve market price: {symbol}"
        )

    if first_tick.time_msc <= 0:
        raise ValueError(
            f"Execution blocked: invalid market tick time for {symbol}."
        )

    deadline = time.monotonic() + timeout_seconds

    while time.monotonic() < deadline:
        time.sleep(poll_seconds)

        updated_tick = mt5.symbol_info_tick(symbol)

        if updated_tick is None:
            continue

        if updated_tick.time_msc <= 0:
            raise ValueError(
                f"Execution blocked: invalid updated market tick time for {symbol}."
            )

        tick_advance_seconds = (
            updated_tick.time_msc - first_tick.time_msc
        ) / 1000.0

        if tick_advance_seconds < 0:
            raise ValueError(
                f"Execution blocked: market tick moved backwards for {symbol}."
            )

        if tick_advance_seconds == 0:
            continue

        if tick_advance_seconds > max_advance_seconds:
            raise ValueError(
                f"Execution blocked: implausible market tick advance for {symbol} "
                f"({tick_advance_seconds:.1f} seconds)."
            )

        return updated_tick

    raise ValueError(
        f"Execution blocked: no fresh market tick detected for {symbol} "
        f"within {timeout_seconds:.1f} seconds."
    )


def calculate_position_size(
    symbol,
    order_type,
    entry_price,
    stop_price,
    risk_percent=DEFAULT_RISK_PERCENT,
    max_lot=DEFAULT_MAX_LOT,
):

    account = mt5.account_info()
    symbol_info = mt5.symbol_info(symbol)

    if account is None:
        raise ValueError("Could not retrieve MT5 account information.")

    if symbol_info is None:
        raise ValueError(f"Could not retrieve symbol information: {symbol}")

    if risk_percent <= 0:
        raise ValueError("Risk percent must be greater than zero.")

    if max_lot <= 0:
        raise ValueError("Maximum lot size must be greater than zero.")

    if order_type not in (
        mt5.ORDER_TYPE_BUY,
        mt5.ORDER_TYPE_SELL,
    ):
        raise ValueError("Only BUY and SELL market orders are supported.")

    if order_type == mt5.ORDER_TYPE_BUY:
        if stop_price >= entry_price:
            raise ValueError(
                "BUY stop-loss must be below the entry price."
            )

    if order_type == mt5.ORDER_TYPE_SELL:
        if stop_price <= entry_price:
            raise ValueError(
                "SELL stop-loss must be above the entry price."
            )

    one_lot_result = mt5.order_calc_profit(
        order_type,
        symbol,
        1.0,
        entry_price,
        stop_price,
    )

    if one_lot_result is None:
        raise ValueError(
            f"Could not calculate stop-loss risk: {mt5.last_error()}"
        )

    one_lot_loss = abs(one_lot_result)

    if one_lot_loss <= 0:
        raise ValueError("Stop-loss risk must be greater than zero.")

    risk_budget = account.balance * risk_percent / 100

    theoretical_lots = risk_budget / one_lot_loss

    capped_lots = min(
        theoretical_lots,
        max_lot,
        symbol_info.volume_max,
    )

    volume_step = symbol_info.volume_step

    if volume_step <= 0:
        raise ValueError("Invalid MT5 volume step.")

    stepped_lots = int(
        (capped_lots + 1e-12) / volume_step
    ) * volume_step

    stepped_lots = round(stepped_lots, 8)

    if stepped_lots < symbol_info.volume_min:
        return 0.0

    return stepped_lots


def build_demo_order_preflight(
    symbol,
    order_type,
    stop_loss_points=DEFAULT_STOP_LOSS_POINTS,
):

    allowed, message = require_demo_execution_environment(symbol)

    if not allowed:
        raise ValueError(message)

    allowed, message = require_no_open_castle_position(symbol)

    if not allowed:
        raise ValueError(message)

    if order_type not in (
        mt5.ORDER_TYPE_BUY,
        mt5.ORDER_TYPE_SELL,
    ):
        raise ValueError("Only BUY and SELL market orders are supported.")

    if stop_loss_points <= 0:
        raise ValueError("Stop-loss points must be greater than zero.")

    symbol_info = mt5.symbol_info(symbol)

    if symbol_info is None:
        raise ValueError(
            f"Could not retrieve symbol information: {symbol}"
        )

    if not symbol_info.visible:
        if not mt5.symbol_select(symbol, True):
            raise ValueError(
                f"Could not select symbol: {symbol}"
            )

    tick = require_fresh_market_tick(symbol)

    if order_type == mt5.ORDER_TYPE_BUY:
        entry_price = tick.ask
        stop_price = (
            entry_price
            - stop_loss_points * symbol_info.point
        )
        direction = "BUY"

    else:
        entry_price = tick.bid
        stop_price = (
            entry_price
            + stop_loss_points * symbol_info.point
        )
        direction = "SELL"

    volume = calculate_position_size(
        symbol,
        order_type,
        entry_price,
        stop_price,
        max_lot=FIRST_DEMO_MAX_LOT,
    )

    if volume <= 0:
        raise ValueError(
            "Calculated position size is below the tradable minimum."
        )

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "price": entry_price,
        "sl": stop_price,
        "deviation": 20,
        "magic": CASTLE_MAGIC_NUMBER,
        "comment": "Nightforce demo preflight",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK,
    }

    check_result = mt5.order_check(request)

    if check_result is None:
        raise ValueError(
            f"MT5 order check failed: {mt5.last_error()}"
        )

    if check_result.retcode != 0:
        raise ValueError(
            "MT5 order check rejected request: "
            f"{check_result.retcode} {check_result.comment}"
        )

    return {
        "direction": direction,
        "request": request,
        "check_result": check_result,
    }


def build_demo_close_preflight(symbol=DEFAULT_SYMBOL):

    allowed, message = require_demo_execution_environment(symbol)

    if not allowed:
        raise ValueError(message)

    position = get_open_castle_position(symbol)

    if position.type == mt5.POSITION_TYPE_BUY:
        close_type = mt5.ORDER_TYPE_SELL
        direction = "SELL"

    elif position.type == mt5.POSITION_TYPE_SELL:
        close_type = mt5.ORDER_TYPE_BUY
        direction = "BUY"

    else:
        raise ValueError(
            f"Unsupported Castle position type: {position.type}"
        )

    symbol_info = mt5.symbol_info(symbol)

    if symbol_info is None:
        raise ValueError(
            f"Could not retrieve symbol information: {symbol}"
        )

    if not symbol_info.visible:
        if not mt5.symbol_select(symbol, True):
            raise ValueError(
                f"Could not select symbol: {symbol}"
            )

    tick = require_fresh_market_tick(symbol)

    if close_type == mt5.ORDER_TYPE_SELL:
        close_price = tick.bid
    else:
        close_price = tick.ask

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": position.volume,
        "type": close_type,
        "position": position.ticket,
        "price": close_price,
        "deviation": 20,
        "magic": CASTLE_MAGIC_NUMBER,
        "comment": "Nightforce demo close",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK,
    }

    check_result = mt5.order_check(request)

    if check_result is None:
        raise ValueError(
            f"MT5 close order check failed: {mt5.last_error()}"
        )

    if check_result.retcode != 0:
        raise ValueError(
            "MT5 close order check rejected request: "
            f"{check_result.retcode} {check_result.comment}"
        )

    return {
        "direction": direction,
        "position": position,
        "request": request,
        "check_result": check_result,
    }


def execute_demo_order(
    symbol,
    order_type,
    arm_token,
    stop_loss_points=DEFAULT_STOP_LOSS_POINTS,
):

    require_demo_execution_armed(arm_token)

    preflight = build_demo_order_preflight(
        symbol,
        order_type,
        stop_loss_points,
    )

    result = mt5.order_send(preflight["request"])

    if result is None:
        raise ValueError(
            f"MT5 order send failed: {mt5.last_error()}"
        )

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        raise ValueError(
            "MT5 demo order was not fully executed: "
            f"{result.retcode} {result.comment}"
        )

    position = retry_position_verification(
        verify_open_castle_position,
        preflight["request"],
    )

    return {
        "direction": preflight["direction"],
        "request": preflight["request"],
        "check_result": preflight["check_result"],
        "result": result,
        "position": position,
    }


def execute_demo_close(
    symbol,
    arm_token,
):

    require_demo_execution_armed(arm_token)

    preflight = build_demo_close_preflight(symbol)

    result = mt5.order_send(preflight["request"])

    if result is None:
        raise ValueError(
            f"MT5 close order send failed: {mt5.last_error()}"
        )

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        raise ValueError(
            "MT5 demo close was not fully executed: "
            f"{result.retcode} {result.comment}"
        )

    close_verified = retry_position_verification(
        verify_closed_castle_position,
        preflight["request"]["symbol"],
    )

    return {
        "direction": preflight["direction"],
        "position": preflight["position"],
        "request": preflight["request"],
        "check_result": preflight["check_result"],
        "result": result,
        "close_verified": close_verified,
    }


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

            print("Invalid choice.")


def show_connection_status():

    print("=" * 70)
    print("MT5 CONNECTION STATUS")
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

        print("Could not connect to MetaTrader 5.")
        print()

        input("Press Enter to continue...")
        return

    account = mt5.account_info()

    if account:

        print("Login:", account.login)
        print("Server:", account.server)
        print("Balance:", account.balance)
        print("Equity:", account.equity)
        print("Currency:", account.currency)

    else:

        print("Could not retrieve account information.")

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

        print()
        print("Could not connect to MetaTrader 5.")
        print()

        input("Press Enter to continue...")
        return

    symbol_info = mt5.symbol_info_tick(symbol)

    if symbol_info:

        print()
        print("Symbol:", symbol)
        print("Bid:", symbol_info.bid)
        print("Ask:", symbol_info.ask)
        print()

    else:

        print()
        print("Could not retrieve market price.")
        print()

    mt5.shutdown()

    input("Press Enter to continue...")


def show_trading_signal():

    print()
    print("=" * 70)
    print("MT5 TRADING SIGNAL")
    print("=" * 70)
    print()

    symbol = input(
        f"Enter symbol (default {DEFAULT_SYMBOL}): "
    ).strip().upper()

    if not symbol:

        symbol = DEFAULT_SYMBOL

    if not mt5.initialize(MT5_PATH):

        print()
        print("Could not connect to MetaTrader 5.")
        print()

        input("Press Enter to continue...")
        return

    symbol_info = mt5.symbol_info(symbol)

    if symbol_info is None:

        print()
        print(f"Symbol not found: {symbol}")
        print()

        mt5.shutdown()
        input("Press Enter to continue...")
        return

    if not symbol_info.visible:

        if not mt5.symbol_select(symbol, True):

            print()
            print(f"Could not select symbol: {symbol}")
            print()

            mt5.shutdown()
            input("Press Enter to continue...")
            return

    result = calculate_signal(symbol)

    strength = result.get("strength", 0)

    if strength < 40:

        strength_level = "WEAK"

    elif strength < 70:

        strength_level = "MODERATE"

    else:

        strength_level = "STRONG"

    print()
    print("Symbol:", symbol)
    print("Timeframe: M15")
    print()

    print("Signal:", result["signal"])
    print("Signal Strength:", f"{strength}/100")
    print("Strength Level:", strength_level)
    print()

    print("Reason:")
    print(result["reason"])
    print()

    if result.get("price") is not None:

        print("Current Price:", result["price"])
        print("10-Candle Average:", result["short_average"])
        print("30-Candle Average:", result["long_average"])
        print(
            "Separation:",
            round(result["average_separation_points"], 1),
            "points"
        )

    print()
    print("WARNING: SIGNAL ONLY")
    print("NO ORDER HAS BEEN CREATED.")
    print()

    mt5.shutdown()

    input("Press Enter to continue...")


def show_risk_settings():

    print("=" * 70)
    print("MT5 TRADING RISK SETTINGS")
    print("=" * 70)
    print()

    print("Trading mode: DEMO / SIMULATION")
    print("Live order execution: DISABLED")
    print()
    print("Default symbol:", DEFAULT_SYMBOL)
    print("Risk per trade:", DEFAULT_RISK_PERCENT, "%")
    print("Maximum lot size:", DEFAULT_MAX_LOT)
    print("Required stop-loss:", DEFAULT_STOP_LOSS_POINTS, "points")
    print()

    print("Safety rules:")
    print("✓ Live order execution is not implemented")
    print("✓ Risk is capped by the maximum lot setting")
    print("✓ Stop-loss is required for future trade logic")
    print("✓ Strategy signals will be added separately")
    print()

    input("Press Enter to continue...")


if __name__ == "__main__":

    trading_bot()

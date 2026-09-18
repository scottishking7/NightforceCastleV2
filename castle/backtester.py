"""Nightforce Strategy Lab backtesting foundation.

Historical strategy testing belongs here.
This module does not place or execute trades.
"""

import MetaTrader5 as mt5

from castle.signal_engine import calculate_ma_signal_from_closes


DEFAULT_SYMBOL = "EURUSD"
DEFAULT_TIMEFRAME = mt5.TIMEFRAME_M15
DEFAULT_BAR_COUNT = 500


def load_historical_bars(
    symbol=DEFAULT_SYMBOL,
    timeframe=DEFAULT_TIMEFRAME,
    bar_count=DEFAULT_BAR_COUNT,
):
    """Load completed historical bars from an initialized MT5 terminal."""

    rates = mt5.copy_rates_from_pos(
        symbol,
        timeframe,
        1,
        bar_count,
    )

    if rates is None:
        return []

    return list(rates)


def replay_ma_signals(bars):
    """Replay the MA strategy through historical bars chronologically."""

    if len(bars) < 30:
        return []

    closes = []
    results = []

    for bar in bars:
        closes.append(float(bar["close"]))

        if len(closes) < 30:
            continue

        signal = calculate_ma_signal_from_closes(closes)

        results.append({
            "time": int(bar["time"]),
            "signal": signal["signal"],
            "price": signal["price"],
            "strength": signal["strength"],
        })

    return results


def simulate_ma_trades(bars):
    """Simulate MA entries and exits at the next completed bar open."""

    if len(bars) < 31:
        return []

    closes = []
    events = []
    previous_signal = None

    for index, bar in enumerate(bars[:-1]):
        closes.append(float(bar["close"]))

        if len(closes) < 30:
            continue

        result = calculate_ma_signal_from_closes(closes)
        current_signal = result["signal"]

        if current_signal == previous_signal:
            continue

        next_bar = bars[index + 1]

        events.append({
            "signal_time": int(bar["time"]),
            "execution_time": int(next_bar["time"]),
            "signal": current_signal,
            "execution_price": float(next_bar["open"]),
        })

        previous_signal = current_signal

    return events


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


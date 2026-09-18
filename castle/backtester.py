"""Nightforce Strategy Lab backtesting foundation.

Historical strategy testing belongs here.
This module does not place or execute trades.
"""

import MetaTrader5 as mt5


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

import MetaTrader5 as mt5


def calculate_signal(symbol="EURUSD"):

    rates = mt5.copy_rates_from_pos(
        symbol,
        mt5.TIMEFRAME_M15,
        0,
        50
    )

    if rates is None or len(rates) < 30:

        return {
            "signal": "WAIT",
            "reason": "Not enough market data."
        }

    closes = [float(rate["close"]) for rate in rates]

    short_average = sum(closes[-10:]) / 10
    long_average = sum(closes[-30:]) / 30
    current_price = closes[-1]

    if short_average > long_average and current_price > short_average:

        return {
            "signal": "BUY",
            "reason": (
                "Short-term average is above the long-term average "
                "and price is above the short-term average."
            ),
            "price": current_price,
            "short_average": short_average,
            "long_average": long_average
        }

    if short_average < long_average and current_price < short_average:

        return {
            "signal": "SELL",
            "reason": (
                "Short-term average is below the long-term average "
                "and price is below the short-term average."
            ),
            "price": current_price,
            "short_average": short_average,
            "long_average": long_average
        }

    return {
        "signal": "WAIT",
        "reason": (
            "The moving-average conditions are not aligned "
            "strongly enough for a directional signal."
        ),
        "price": current_price,
        "short_average": short_average,
        "long_average": long_average
    }

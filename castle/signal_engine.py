import MetaTrader5 as mt5

MIN_AVERAGE_SEPARATION_POINTS = 20


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
            "reason": "Not enough market data.",
            "price": None,
            "short_average": None,
            "long_average": None,
            "average_separation_points": 0,
            "strength": 0,
            "strength_level": "WEAK",
            "conditions": [
                "Not enough market data to calculate the signal."
            ]
        }

    closes = [float(rate["close"]) for rate in rates]

    short_average = sum(closes[-10:]) / 10
    long_average = sum(closes[-30:]) / 30
    current_price = closes[-1]

    average_separation_points = (
        abs(short_average - long_average) / 0.00001
    )

    strength = min(
        100,
        int(average_separation_points / 2)
    )

    if strength < 40:

        strength_level = "WEAK"

    elif strength < 70:

        strength_level = "MODERATE"

    else:

        strength_level = "STRONG"

    conditions = []

    if short_average > long_average:

        conditions.append(
            "✓ Short-term average is above the long-term average."
        )

        trend = "BULLISH"

    else:

        conditions.append(
            "✓ Short-term average is below the long-term average."
        )

        trend = "BEARISH"

    if current_price > short_average:

        conditions.append(
            "✓ Current price is above the short-term average."
        )

        price_position = "ABOVE"

    else:

        conditions.append(
            "✓ Current price is below the short-term average."
        )

        price_position = "BELOW"

    if average_separation_points >= MIN_AVERAGE_SEPARATION_POINTS:

        conditions.append(
            "✓ Average separation is above the minimum threshold."
        )

        separation_ok = True

    else:

        conditions.append(
            "✗ Average separation is below the minimum threshold."
        )

        separation_ok = False

    if (
        trend == "BULLISH"
        and price_position == "ABOVE"
        and separation_ok
    ):

        return {
            "signal": "BUY",
            "reason": (
                "Short-term average is above the long-term average "
                "and price is above the short-term average."
            ),
            "price": current_price,
            "short_average": short_average,
            "long_average": long_average,
            "average_separation_points": average_separation_points,
            "strength": strength,
            "strength_level": strength_level,
            "conditions": conditions
        }

    if (
        trend == "BEARISH"
        and price_position == "BELOW"
        and separation_ok
    ):

        return {
            "signal": "SELL",
            "reason": (
                "Short-term average is below the long-term average "
                "and price is below the short-term average."
            ),
            "price": current_price,
            "short_average": short_average,
            "long_average": long_average,
            "average_separation_points": average_separation_points,
            "strength": strength,
            "strength_level": strength_level,
            "conditions": conditions
        }

    return {
        "signal": "WAIT",
        "reason": (
            "The moving-average conditions are not aligned "
            "strongly enough for a directional signal."
        ),
        "price": current_price,
        "short_average": short_average,
        "long_average": long_average,
        "average_separation_points": average_separation_points,
        "strength": strength,
        "strength_level": strength_level,
        "conditions": conditions
    }
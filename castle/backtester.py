"""Nightforce Strategy Lab backtesting foundation.

Historical strategy testing belongs here.
This module does not place or execute trades.
"""

import MetaTrader5 as mt5

from castle.signal_engine import calculate_ma_signal_from_closes
from castle.strategy_lab import get_confirmation_bars


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


def load_historical_bars_range(
    start_time,
    end_time,
    symbol=DEFAULT_SYMBOL,
    timeframe=DEFAULT_TIMEFRAME,
):
    """Load a fixed historical bar range from an initialized MT5 terminal."""

    rates = mt5.copy_rates_range(
        symbol,
        timeframe,
        start_time,
        end_time,
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


def simulate_ma_trades_with_confirmation(
    bars,
    confirmation_bars,
):
    """Simulate MA trades after a signal persists for completed bars."""

    if len(bars) < 31:
        return []

    if confirmation_bars < 1:
        raise ValueError(
            "confirmation_bars must be at least 1"
        )

    closes = []
    events = []
    previous_confirmed_signal = None
    candidate_signal = None
    candidate_count = 0

    for index, bar in enumerate(bars[:-1]):
        closes.append(float(bar["close"]))

        if len(closes) < 30:
            continue

        result = calculate_ma_signal_from_closes(closes)
        current_signal = result["signal"]

        if current_signal == candidate_signal:
            candidate_count += 1
        else:
            candidate_signal = current_signal
            candidate_count = 1

        if candidate_count < confirmation_bars:
            continue

        if current_signal == previous_confirmed_signal:
            continue

        next_bar = bars[index + 1]

        events.append({
            "signal_time": int(bar["time"]),
            "execution_time": int(next_bar["time"]),
            "signal": current_signal,
            "execution_price": float(next_bar["open"]),
        })

        previous_confirmed_signal = current_signal

    return events


def simulate_registered_ma_strategy(bars, strategy_id):
    """Simulate a registered MA strategy using Strategy Lab metadata."""

    confirmation_bars = get_confirmation_bars(strategy_id)

    return simulate_ma_trades_with_confirmation(
        bars,
        confirmation_bars,
    )


def pair_ma_trades(events):
    """Pair simulated MA entry and exit events into completed trades."""

    trades = []
    open_trade = None

    for event in events:
        signal = event["signal"]

        if open_trade is None:
            if signal in ("BUY", "SELL"):
                open_trade = {
                    "direction": signal,
                    "entry_time": event["execution_time"],
                    "entry_price": event["execution_price"],
                }

            continue

        if signal != "WAIT":
            continue

        trades.append({
            "direction": open_trade["direction"],
            "entry_time": open_trade["entry_time"],
            "entry_price": open_trade["entry_price"],
            "exit_time": event["execution_time"],
            "exit_price": event["execution_price"],
        })

        open_trade = None

    return trades


def calculate_trade_price_moves(trades):
    """Add direction-aware raw price movement to completed trades."""

    results = []

    for trade in trades:
        result = trade.copy()

        if trade["direction"] == "BUY":
            price_move = (
                trade["exit_price"]
                - trade["entry_price"]
            )

        elif trade["direction"] == "SELL":
            price_move = (
                trade["entry_price"]
                - trade["exit_price"]
            )

        else:
            raise ValueError(
                f"Unknown trade direction: {trade['direction']}"
            )

        result["price_move"] = price_move
        results.append(result)

    return results


def apply_spread_costs(
    trades,
    point_size,
    spread_points,
):
    """Apply a configurable round-trip spread cost to trade results."""

    if point_size <= 0:
        raise ValueError("point_size must be greater than zero")

    if spread_points < 0:
        raise ValueError("spread_points cannot be negative")

    spread_cost = point_size * spread_points
    results = []

    for trade in trades:
        if "price_move" not in trade:
            raise ValueError(
                "Trade must contain price_move before spread costs are applied"
            )

        result = trade.copy()
        result["spread_points"] = spread_points
        result["spread_cost"] = spread_cost
        result["net_price_move"] = (
            trade["price_move"] - spread_cost
        )

        results.append(result)

    return results


def evaluate_registered_ma_strategy(
    bars,
    strategy_id,
    point_size,
    spread_points,
):
    """Evaluate a registered MA strategy on supplied historical bars."""

    events = simulate_registered_ma_strategy(
        bars,
        strategy_id,
    )

    trades = pair_ma_trades(events)
    raw_trades = calculate_trade_price_moves(trades)

    net_trades = apply_spread_costs(
        raw_trades,
        point_size,
        spread_points,
    )

    summary = summarize_trade_performance(net_trades)

    return {
        "strategy_id": strategy_id,
        "bar_count": len(bars),
        "event_count": len(events),
        "raw_total_price_move": sum(
            trade["price_move"]
            for trade in raw_trades
        ),
        "spread_points": spread_points,
        **summary,
    }


def evaluate_registered_ma_periods(
    periods,
    strategy_id,
    point_size,
    spread_points,
):
    """Evaluate a registered MA strategy across named historical periods."""

    results = {}

    for period_name, bars in periods.items():
        results[period_name] = evaluate_registered_ma_strategy(
            bars,
            strategy_id,
            point_size,
            spread_points,
        )

    return results


def summarize_period_results(results):
    """Summarize registered strategy results across historical periods."""

    if not results:
        return {
            "period_count": 0,
            "positive_periods": 0,
            "negative_periods": 0,
            "flat_periods": 0,
            "completed_trades": 0,
            "raw_total_price_move": 0.0,
            "total_net_price_move": 0.0,
        }

    net_totals = [
        result["total_net_price_move"]
        for result in results.values()
    ]

    return {
        "period_count": len(results),
        "positive_periods": sum(
            value > 0
            for value in net_totals
        ),
        "negative_periods": sum(
            value < 0
            for value in net_totals
        ),
        "flat_periods": sum(
            value == 0
            for value in net_totals
        ),
        "completed_trades": sum(
            result["completed_trades"]
            for result in results.values()
        ),
        "raw_total_price_move": sum(
            result["raw_total_price_move"]
            for result in results.values()
        ),
        "total_net_price_move": sum(net_totals),
    }


def summarize_trade_performance(trades):
    """Summarize completed trades using net price movement."""

    if not trades:
        return {
            "completed_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "flat_trades": 0,
            "win_rate": 0.0,
            "total_net_price_move": 0.0,
            "average_net_price_move": 0.0,
            "maximum_drawdown": 0.0,
            "profit_factor": None,
        }

    net_moves = []

    for trade in trades:
        if "net_price_move" not in trade:
            raise ValueError(
                "Trade must contain net_price_move before summarizing performance"
            )

        net_moves.append(trade["net_price_move"])

    winning_trades = sum(
        move > 0
        for move in net_moves
    )

    losing_trades = sum(
        move < 0
        for move in net_moves
    )

    flat_trades = sum(
        move == 0
        for move in net_moves
    )

    completed_trades = len(net_moves)
    total_net_price_move = sum(net_moves)

    gross_profit = sum(
        move
        for move in net_moves
        if move > 0
    )

    gross_loss = abs(
        sum(
            move
            for move in net_moves
            if move < 0
        )
    )

    if gross_loss == 0:
        profit_factor = None
    else:
        profit_factor = (
            gross_profit
            / gross_loss
        )

    cumulative_net_move = 0.0
    peak_net_move = 0.0
    maximum_drawdown = 0.0

    for move in net_moves:
        cumulative_net_move += move
        peak_net_move = max(
            peak_net_move,
            cumulative_net_move,
        )

        drawdown = (
            peak_net_move
            - cumulative_net_move
        )

        maximum_drawdown = max(
            maximum_drawdown,
            drawdown,
        )

    return {
        "completed_trades": completed_trades,
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "flat_trades": flat_trades,
        "win_rate": (
            winning_trades
            / completed_trades
            * 100
        ),
        "total_net_price_move": total_net_price_move,
        "average_net_price_move": (
            total_net_price_move
            / completed_trades
        ),
        "maximum_drawdown": maximum_drawdown,
        "profit_factor": profit_factor,
    }


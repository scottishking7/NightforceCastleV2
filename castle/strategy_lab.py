"""Nightforce Strategy Lab.

Strategy definitions and research metadata live here.
Trade execution does not belong in this module.
"""

STRATEGIES = {
    "ma_trend": {
        "name": "MA Trend",
        "description": (
            "Existing Nightforce 10/30 moving-average trend strategy."
        ),
        "timeframe": "M15",
        "status": "ACTIVE_BASELINE",
    },
    "ma_trend_confirmed_3": {
        "name": "MA Trend - 3 Bar Confirmation",
        "description": (
            "Experimental 10/30 MA trend strategy requiring "
            "three consecutive matching completed-bar signals."
        ),
        "timeframe": "M15",
        "confirmation_bars": 3,
        "status": "EXPERIMENTAL",
    },
}

RESEARCH_FINDINGS = {
    "eurusd_m15_volatility_regimes": {
        "name": "EURUSD M15 Volatility Regimes",
        "description": (
            "Recent 20-bar average high-low volatility was associated "
            "with the magnitude of the subsequent 5-bar price move in "
            "both 2025 and 2026 research samples. The relationship "
            "replicated with non-overlapping forward observations but "
            "did not provide a reliable directional signal."
        ),
        "symbol": "EURUSD",
        "timeframe": "M15",
        "volatility_lookback_bars": 20,
        "forward_measurement_bars": 5,
        "point_size": 0.00001,
        "regime_boundaries_points": (
            50.05,
            67.65,
            90.75,
        ),
        "boundary_source": "2025 research sample",
        "validation_periods": (
            "2025",
            "2026-01 through 2026-08",
        ),
        "status": "REPLICATED_RESEARCH_FINDING",
        "directional_signal": False,
    },
    "eurusd_m15_utc_time_blocks": {
        "name": "EURUSD M15 UTC Time Blocks",
        "description": (
            "UTC time block added information about the magnitude of "
            "the subsequent 5-bar price move after controlling for "
            "the 20-bar volatility regime. The broad relationship "
            "replicated in 2025 and 2026 using non-overlapping "
            "forward observations and did not provide a directional "
            "signal."
        ),
        "symbol": "EURUSD",
        "timeframe": "M15",
        "time_basis": "UTC",
        "time_blocks": (
            "00-05",
            "06-11",
            "12-17",
            "18-23",
        ),
        "volatility_lookback_bars": 20,
        "forward_measurement_bars": 5,
        "non_overlapping_forward_windows": True,
        "relative_move_vs_regime_average": {
            "2025": (
                -6.8,
                16.1,
                18.6,
                -27.9,
            ),
            "2026-01 through 2026-08": (
                -11.4,
                15.9,
                19.1,
                -23.9,
            ),
        },
        "validation_periods": (
            "2025",
            "2026-01 through 2026-08",
        ),
        "status": "REPLICATED_RESEARCH_FINDING",
        "directional_signal": False,
    },
}



def get_strategy(strategy_id):
    """Return a Strategy Lab definition by its identifier."""

    return STRATEGIES.get(strategy_id)


def get_confirmation_bars(strategy_id):
    """Return the registered MA confirmation-bar count."""

    strategy = get_strategy(strategy_id)

    if strategy is None:
        raise ValueError(
            f"Unknown strategy: {strategy_id}"
        )

    return strategy.get("confirmation_bars", 1)


def list_strategies():
    """Return all currently registered Strategy Lab definitions."""

    return STRATEGIES.copy()

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
    "eurusd_m15_ma_trend_confirmed_3": {
        "name": "EURUSD M15 3-Bar Confirmed MA Research",
        "description": (
            "The 10/30 moving-average strategy with three-bar "
            "confirmation did not demonstrate a robust executable "
            "edge across the 2025 and 2026 research periods. "
            "Entry filters and early-exit diagnostics produced "
            "interesting state relationships, but tested executable "
            "interventions did not establish consistent profitability."
        ),
        "symbol": "EURUSD",
        "timeframe": "M15",
        "strategy_id": "ma_trend_confirmed_3",
        "validation_periods": (
            "2025",
            "2026-01 through 2026-08",
        ),
        "forward_direction_horizons_bars": (
            1,
            3,
            5,
            10,
            20,
        ),
        "forward_direction_average_points": {
            "2025": (
                -0.35,
                -1.96,
                -3.05,
                -7.54,
                -3.94,
            ),
            "2026-01 through 2026-08": (
                0.05,
                1.59,
                3.00,
                2.71,
                3.48,
            ),
        },
        "research_conclusion": (
            "Retain as a benchmark; do not promote to live trading."
        ),
        "status": "RESEARCH_CLOSED_NO_ROBUST_EDGE",
    },
    "eurusd_m15_new_low_reversion": {
        "name": "EURUSD M15 New-Low Reversion",
        "description": (
            "Independent closes below the previous 20-bar low showed "
            "a modest upward reversion over the subsequent 5 bars in "
            "both the 2025 and 2026 research samples. A causal "
            "next-open implementation remained slightly profitable "
            "with a 5-point spread overall, but profitability was "
            "cost-sensitive, concentrated in large winners, and not "
            "stable across chronological subperiods."
        ),
        "symbol": "EURUSD",
        "timeframe": "M15",
        "lookback_bars": 20,
        "forward_measurement_bars": 5,
        "independent_event_separation_bars": 5,
        "point_size": 0.00001,
        "independent_event_average_upward_points": {
            "2025": 5.96,
            "2026-01 through 2026-08": 6.64,
        },
        "independent_event_reversal_percent": {
            "2025": 54.87,
            "2026-01 through 2026-08": 52.05,
        },
        "tested_execution": (
            "BUY next bar open after a qualifying completed-bar "
            "signal; hold 5 complete bars; exit following bar open."
        ),
        "tested_spread_points": 5.0,
        "tested_net_expectancy_points": {
            "2025": 1.94,
            "2026-01 through 2026-08": 1.49,
        },
        "tested_profit_factor": {
            "2025": 1.042,
            "2026-01 through 2026-08": 1.040,
        },
        "research_conclusion": (
            "Preserve the replicated structural reversion finding, "
            "but close the tested executable strategy because the "
            "edge was thin, cost-sensitive, winner-concentrated, "
            "and chronologically unstable."
        ),
        "validation_periods": (
            "2025",
            "2026-01 through 2026-08",
        ),
        "status": "REPLICATED_FINDING_EXECUTION_CLOSED",
        "promote_to_trading": False,
    },
    "eurusd_m15_one_bar_range_persistence": {
        "name": "EURUSD M15 One-Bar Range Persistence",
        "description": (
            "The high-low range of the most recently completed M15 "
            "bar was strongly associated with the high-low range of "
            "the following bar in both the 2025 and 2026 research "
            "samples. The relationship remained monotonically ordered "
            "after controlling for the existing 20-bar volatility "
            "regime, indicating incremental short-horizon volatility "
            "information rather than only the broader regime effect. "
            "The finding predicts movement magnitude, not direction."
        ),
        "symbol": "EURUSD",
        "timeframe": "M15",
        "point_size": 0.00001,
        "forward_measurement_bars": 1,
        "non_overlapping_observations": True,
        "range_boundaries_points": (
            41.0,
            61.0,
            92.0,
        ),
        "boundary_source": "2025 research sample",
        "average_next_range_points": {
            "2025": (
                43.79,
                61.05,
                78.32,
                120.87,
            ),
            "2026-01 through 2026-08": (
                37.44,
                52.95,
                70.13,
                101.53,
            ),
        },
        "median_next_range_points": {
            "2025": (
                38.0,
                54.0,
                69.0,
                101.0,
            ),
            "2026-01 through 2026-08": (
                33.0,
                47.0,
                62.0,
                89.0,
            ),
        },
        "controlled_for_20_bar_volatility": True,
        "controlled_relationship": (
            "Within every frozen 20-bar volatility quartile, "
            "next-bar average and median range increased monotonically "
            "from current-bar range Q1 through Q4 in both validation "
            "periods."
        ),
        "validation_periods": (
            "2025",
            "2026-01 through 2026-08",
        ),
        "research_conclusion": (
            "Preserve as a replicated incremental volatility feature. "
            "Do not interpret it as a directional trading signal."
        ),
        "status": "REPLICATED_RESEARCH_FINDING",
        "directional_signal": False,
        "promote_to_trading": False,
    },
    "eurusd_m15_volatility_acceleration": {
        "name": "EURUSD M15 Volatility Acceleration",
        "description": (
            "The ratio of average high-low range over the most recent "
            "5 completed M15 bars to the preceding 15 completed bars "
            "was associated with the magnitude of the subsequent "
            "5-bar price move in both the 2025 and 2026 research "
            "samples. Higher volatility acceleration generally "
            "preceded larger absolute price movement. The relationship "
            "remained broadly ordered after controlling for the "
            "existing 20-bar absolute-volatility regime."
        ),
        "symbol": "EURUSD",
        "timeframe": "M15",
        "point_size": 0.00001,
        "total_lookback_bars": 20,
        "recent_bars": 5,
        "preceding_bars": 15,
        "forward_measurement_bars": 5,
        "non_overlapping_forward_windows": True,
        "acceleration_boundaries": (
            0.7314,
            0.9495,
            1.2736,
        ),
        "boundary_source": "2025 research sample",
        "average_future_absolute_points": {
            "2025": (
                68.44,
                79.92,
                88.05,
                104.64,
            ),
            "2026-01 through 2026-08": (
                57.28,
                63.56,
                68.95,
                77.44,
            ),
        },
        "median_future_absolute_points": {
            "2025": (
                47.0,
                54.0,
                60.0,
                74.0,
            ),
            "2026-01 through 2026-08": (
                34.0,
                44.0,
                50.0,
                53.0,
            ),
        },
        "controlled_for_20_bar_volatility": True,
        "controlled_relationship": (
            "Within each frozen 20-bar volatility quartile, higher "
            "acceleration was broadly associated with larger future "
            "absolute movement in both validation periods. Minor "
            "adjacent-quartile irregularities did not alter the broad "
            "Q1-to-Q4 relationship."
        ),
        "validation_periods": (
            "2025",
            "2026-01 through 2026-08",
        ),
        "research_conclusion": (
            "Preserve as a replicated incremental volatility feature. "
            "It describes volatility magnitude and acceleration, not "
            "future price direction."
        ),
        "status": "REPLICATED_RESEARCH_FINDING",
        "directional_signal": False,
        "promote_to_trading": False,
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

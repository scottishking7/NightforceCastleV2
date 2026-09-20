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
        "persistence_horizons_bars": (
            1,
            2,
            3,
            5,
            10,
        ),
        "persistence_test_spacing_bars": 11,
        "persistence_average_range_points": {
            "2025": {
                1: (43.87, 60.89, 80.17, 115.44),
                2: (46.02, 60.40, 81.52, 117.66),
                3: (47.06, 62.26, 78.53, 114.99),
                5: (51.48, 64.65, 78.73, 108.63),
                10: (56.55, 66.01, 76.45, 100.56),
            },
            "2026-01 through 2026-08": {
                1: (39.85, 55.03, 75.47, 106.13),
                2: (40.58, 58.58, 69.34, 94.50),
                3: (40.62, 57.61, 70.35, 94.43),
                5: (45.11, 57.45, 72.80, 88.57),
                10: (51.06, 58.88, 66.64, 83.34),
            },
        },
        "persistence_median_range_points": {
            "2025": {
                1: (40.0, 54.0, 71.0, 99.5),
                2: (40.0, 53.0, 70.0, 98.5),
                3: (40.0, 54.0, 67.0, 96.5),
                5: (40.0, 53.0, 66.0, 91.0),
                10: (47.0, 57.0, 63.0, 82.5),
            },
            "2026-01 through 2026-08": {
                1: (34.0, 49.0, 65.0, 92.0),
                2: (36.0, 49.0, 60.0, 85.0),
                3: (35.0, 49.0, 61.0, 82.0),
                5: (37.0, 48.0, 63.0, 80.0),
                10: (42.0, 48.0, 56.0, 67.0),
            },
        },
        "persistence_relationship": (
            "Using the same frozen range boundaries and independent "
            "11-bar-spaced observations, average and median future "
            "bar range remained monotonically ordered from Q1 through "
            "Q4 at horizons 1, 2, 3, 5, and 10 in both validation "
            "periods. The separation narrowed with horizon, consistent "
            "with a persistent but decaying short-term volatility state."
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
    "eurusd_m15_candle_body_fraction": {
        "name": "EURUSD M15 Candle Body Fraction",
        "description": (
            "Candle body fraction, defined as absolute close-open "
            "distance divided by the full high-low range of the "
            "completed M15 bar, contained incremental information "
            "about the following bar's high-low range after controlling "
            "for current-bar range. Within frozen current-range "
            "quartiles, smaller-body and more wick-heavy candles "
            "generally preceded larger next-bar ranges than candles "
            "with larger body fractions in both validation periods. "
            "The unconditional relationship was weak, so this finding "
            "is specifically conditional on current-bar range."
        ),
        "symbol": "EURUSD",
        "timeframe": "M15",
        "point_size": 0.00001,
        "forward_measurement_bars": 1,
        "non_overlapping_observations": True,
        "body_fraction_definition": (
            "abs(close - open) / (high - low)"
        ),
        "body_fraction_boundaries": (
            0.2375,
            0.4557,
            0.6667,
        ),
        "body_boundary_source": "2025 research sample",
        "controlled_for_current_bar_range": True,
        "range_boundaries_points": (
            41.0,
            61.0,
            92.0,
        ),
        "range_boundary_source": (
            "Frozen existing one-bar range persistence boundaries"
        ),
        "controlled_average_next_range_points": {
            "2025": {
                "range_q1": (45.06, 42.69, 43.51, 40.44),
                "range_q2": (65.54, 63.04, 59.16, 53.10),
                "range_q3": (86.55, 77.39, 76.69, 73.40),
                "range_q4": (134.11, 124.28, 123.04, 111.84),
            },
            "2026-01 through 2026-08": {
                "range_q1": (39.52, 36.65, 36.38, 32.60),
                "range_q2": (55.62, 54.44, 51.97, 46.67),
                "range_q3": (73.79, 75.93, 69.70, 62.49),
                "range_q4": (113.26, 100.96, 97.88, 99.32),
            },
        },
        "controlled_median_next_range_points": {
            "2025": {
                "range_q1": (39.0, 38.0, 38.0, 36.0),
                "range_q2": (57.0, 56.0, 53.0, 47.0),
                "range_q3": (77.0, 69.0, 69.0, 64.0),
                "range_q4": (112.0, 106.0, 102.0, 94.0),
            },
            "2026-01 through 2026-08": {
                "range_q1": (35.0, 33.0, 32.0, 29.0),
                "range_q2": (50.0, 50.0, 46.0, 40.0),
                "range_q3": (65.0, 67.0, 61.0, 56.0),
                "range_q4": (99.0, 90.0, 85.0, 88.5),
            },
        },
        "controlled_relationship": (
            "Within every frozen current-bar range quartile, the "
            "lowest body-fraction quartile had a larger average "
            "next-bar range than the highest body-fraction quartile "
            "in both validation periods. The broad inverse relationship "
            "was replicated, with minor adjacent-quartile irregularities."
        ),
        "dual_control_for_20_bar_volatility_and_range": True,
        "volatility_boundaries_points": (
            50.05,
            67.65,
            90.75,
        ),
        "volatility_boundary_source": (
            "Frozen existing 20-bar volatility regime boundaries"
        ),
        "dual_control_method": (
            "For each validation period separately, observations were "
            "assigned to frozen 20-bar-volatility and current-bar-range "
            "quartiles. Next-bar range was residualized against the "
            "mean next-bar range of its volatility-by-range cell, then "
            "the residuals were grouped by the frozen body-fraction "
            "quartiles. Cell baselines were estimated within each "
            "validation period, so this is a replicated conditional "
            "association rather than an out-of-sample prediction model."
        ),
        "dual_control_average_residual_points": {
            "2025": (
                4.76,
                0.09,
                -0.15,
                -4.74,
            ),
            "2026-01 through 2026-08": (
                2.66,
                1.02,
                -0.96,
                -3.28,
            ),
        },
        "dual_control_median_residual_points": {
            "2025": (
                -4.83,
                -7.55,
                -8.01,
                -12.14,
            ),
            "2026-01 through 2026-08": (
                -3.20,
                -3.96,
                -6.55,
                -8.36,
            ),
        },
        "dual_control_relationship": (
            "Average and median residual next-bar range decreased "
            "monotonically from body-fraction Q1 through Q4 in both "
            "validation periods after simultaneous control for the "
            "frozen 20-bar volatility regime and current-bar range."
        ),
        "triple_control_for_volatility_range_and_acceleration": True,
        "acceleration_boundaries": (
            0.7314,
            0.9495,
            1.2736,
        ),
        "acceleration_boundary_source": (
            "Frozen existing volatility acceleration boundaries"
        ),
        "triple_control_method": (
            "For each validation period separately, observations were "
            "assigned to frozen 20-bar-volatility, current-bar-range, "
            "and volatility-acceleration quartiles. Next-bar range was "
            "residualized against the mean next-bar range of its exact "
            "volatility-by-range-by-acceleration cell, then residuals "
            "were grouped by the frozen body-fraction quartiles. Cell "
            "baselines were estimated within each validation period, "
            "so this is a replicated conditional association rather "
            "than an out-of-sample prediction model."
        ),
        "triple_control_populated_cells": {
            "2025": 63,
            "2026-01 through 2026-08": 62,
        },
        "triple_control_average_residual_points": {
            "2025": (
                2.73,
                2.40,
                -2.28,
                -2.83,
            ),
            "2026-01 through 2026-08": (
                2.74,
                0.40,
                -0.55,
                -3.03,
            ),
        },
        "triple_control_median_residual_points": {
            "2025": (
                -5.08,
                -4.96,
                -8.63,
                -10.63,
            ),
            "2026-01 through 2026-08": (
                -4.35,
                -6.39,
                -6.54,
                -10.07,
            ),
        },
        "triple_control_relationship": (
            "The inverse body-fraction relationship remained after "
            "simultaneous control for frozen 20-bar volatility, "
            "current-bar range, and volatility acceleration. Average "
            "residual next-bar range decreased across body-fraction "
            "quartiles in both periods, with 2026 fully monotonic and "
            "2025 showing the same broad Q1-to-Q4 structure. Median "
            "residuals were also broadly supportive."
        ),
        "validation_periods": (
            "2025",
            "2026-01 through 2026-08",
        ),
        "research_conclusion": (
            "Preserve as a replicated incremental short-horizon "
            "volatility feature. The inverse body-fraction relationship "
            "survived simultaneous control for current-bar range, the "
            "broader 20-bar volatility regime, and volatility "
            "acceleration. It predicts movement magnitude, not price "
            "direction."
        ),
        "status": "REPLICATED_RESEARCH_FINDING",
        "directional_signal": False,
        "promote_to_trading": False,
    },
    "eurusd_m15_inside_outside_range_structure": {
        "name": "EURUSD M15 Inside vs Outside Range Structure",
        "description": (
            "Inside-versus-outside candle range structure contained "
            "incremental information about the following M15 bar's "
            "high-low range after controlling for current-bar range. "
            "Unconditionally, outside bars appeared to precede larger "
            "next-bar ranges in the 2025 discovery sample, but outside "
            "bars also had systematically larger current ranges. After "
            "range control, inside bars generally preceded larger "
            "next-bar ranges than outside bars in both validation "
            "periods."
        ),
        "symbol": "EURUSD",
        "timeframe": "M15",
        "point_size": 0.00001,
        "forward_measurement_bars": 1,
        "non_overlapping_observations": True,
        "inside_definition": (
            "current high <= previous high and current low >= previous low"
        ),
        "outside_definition": (
            "current high > previous high and current low < previous low"
        ),
        "range_boundaries_points": (
            41.0,
            61.0,
            92.0,
        ),
        "range_boundary_source": (
            "Frozen existing one-bar range persistence boundaries"
        ),
        "controlled_for_current_bar_range": True,
        "range_quartile_average_next_range_points": {
            "2025": {
                "range_q1": {
                    "inside": 43.66,
                    "outside": 36.67,
                },
                "range_q2": {
                    "inside": 70.83,
                    "outside": 50.50,
                },
                "range_q3": {
                    "inside": 90.09,
                    "outside": 66.07,
                },
                "range_q4": {
                    "inside": 138.94,
                    "outside": 123.11,
                },
            },
            "2026-01 through 2026-08": {
                "range_q1": {
                    "inside": 41.18,
                    "outside": 43.29,
                },
                "range_q2": {
                    "inside": 62.85,
                    "outside": 49.14,
                },
                "range_q3": {
                    "inside": 88.21,
                    "outside": 67.12,
                },
                "range_q4": {
                    "inside": 121.57,
                    "outside": 117.53,
                },
            },
        },
        "range_quartile_median_next_range_points": {
            "2025": {
                "range_q1": {
                    "inside": 39.0,
                    "outside": 30.0,
                },
                "range_q2": {
                    "inside": 64.0,
                    "outside": 44.0,
                },
                "range_q3": {
                    "inside": 79.0,
                    "outside": 59.0,
                },
                "range_q4": {
                    "inside": 118.0,
                    "outside": 94.0,
                },
            },
            "2026-01 through 2026-08": {
                "range_q1": {
                    "inside": 36.0,
                    "outside": 34.0,
                },
                "range_q2": {
                    "inside": 58.0,
                    "outside": 45.0,
                },
                "range_q3": {
                    "inside": 79.0,
                    "outside": 59.0,
                },
                "range_q4": {
                    "inside": 105.0,
                    "outside": 89.0,
                },
            },
        },
        "fine_range_matching": True,
        "fine_range_bin_width_points": 10,
        "fine_range_matching_method": (
            "Inside and outside observations were compared within fixed "
            "10-point current-range bins. Only bins containing both "
            "structures were retained. Each bin's difference was the "
            "mean next-bar range after inside bars minus the mean "
            "next-bar range after outside bars. The aggregate difference "
            "was weighted by the smaller inside/outside count in each "
            "matched bin."
        ),
        "fine_range_matching_results": {
            "2025": {
                "matched_bins": 32,
                "matched_weight": 1028,
                "inside_higher_bins": 29,
                "outside_higher_bins": 3,
                "weighted_average_difference_points": 22.98,
                "median_bin_difference_points": 26.0,
            },
            "2026-01 through 2026-08": {
                "matched_bins": 21,
                "matched_weight": 631,
                "inside_higher_bins": 19,
                "outside_higher_bins": 2,
                "weighted_average_difference_points": 14.43,
                "median_bin_difference_points": 17.80,
            },
        },
        "controlled_relationship": (
            "After controlling for current-bar range, inside bars "
            "generally preceded larger next-bar ranges than outside "
            "bars in both validation periods. Fine 10-point range "
            "matching preserved the relationship in 29 of 32 matched "
            "2025 bins and 19 of 21 matched 2026 bins, with positive "
            "weighted-average and median bin differences in both "
            "periods."
        ),
        "validation_periods": (
            "2025",
            "2026-01 through 2026-08",
        ),
        "research_conclusion": (
            "Preserve as a replicated incremental short-horizon "
            "volatility-structure finding. The inside-versus-outside "
            "relationship survived substantially finer current-range "
            "matching in both validation periods. It describes future "
            "movement magnitude, not price direction, and has not been "
            "tested as an executable trading strategy."
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
        "dual_control_for_20_bar_volatility_and_range": True,
        "range_boundaries_points": (
            41.0,
            61.0,
            92.0,
        ),
        "range_boundary_source": (
            "Frozen existing one-bar range persistence boundaries"
        ),
        "dual_control_method": (
            "For each validation period separately, observations were "
            "assigned to frozen 20-bar-volatility and current-bar-range "
            "quartiles. Future 5-bar absolute movement was residualized "
            "against the mean future movement of its volatility-by-range "
            "cell, then residuals were grouped by the frozen acceleration "
            "quartiles. Cell baselines were estimated within each "
            "validation period, so this is a replicated conditional "
            "association rather than an out-of-sample prediction model."
        ),
        "dual_control_average_residual_points": {
            "2025": (
                -6.30,
                -1.34,
                -0.03,
                7.66,
            ),
            "2026-01 through 2026-08": (
                -3.24,
                -0.16,
                -0.66,
                4.16,
            ),
        },
        "dual_control_median_residual_points": {
            "2025": (
                -19.47,
                -18.57,
                -20.47,
                -16.58,
            ),
            "2026-01 through 2026-08": (
                -20.62,
                -13.00,
                -15.51,
                -12.62,
            ),
        },
        "dual_control_relationship": (
            "Average residual future movement preserved the broad "
            "positive Q1-to-Q4 acceleration relationship in both "
            "validation periods after simultaneous control for frozen "
            "20-bar volatility and current-bar range. The 2025 averages "
            "were monotonic; 2026 had a small Q2-to-Q3 inversion. Median "
            "residuals were noisier and were not monotonically ordered."
        ),
        "validation_periods": (
            "2025",
            "2026-01 through 2026-08",
        ),
        "research_conclusion": (
            "Preserve as a replicated incremental volatility feature. "
            "The broad average acceleration relationship survived "
            "simultaneous control for 20-bar volatility and current-bar "
            "range, although median residuals were less orderly. It "
            "describes volatility magnitude and acceleration, not future "
            "price direction."
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
